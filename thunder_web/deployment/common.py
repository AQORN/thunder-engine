# @author: Geo Varghese
# @create_date: 4-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 4-Mar-2015
# @linking to other page: 
# @description: Common deployment functions

# importing required modules
from cloud.models import *
from cloud.common import *
from cloud.views import *
from deployment.environment import *
from deployment.databag import *
from deployment.role import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import *
import subprocess
from pprint import pprint
from network.functions import *
import datetime

def installOpenstackOS(nodeInfo, envName):
    '''
    function to install main os
    nodeInfo - The node information object
    envName  -  the name of the chef environment
    @return installStatus  The install status of node
    '''
   
    from cloud.common import * 
    installStatus = {}
    installStatus['jobStatus'] = 'S'
    installStatus['errorMsg'] = ''
    errorMsg = ''    
    
    # if node is not prepared
    if not nodeInfo.currentos:
        
        try:
            
            # network card details
            nicName, deviceIp, netDeviceId, netDeviceMac = getNodeNetworkNIC(nodeInfo.id, "A")
            hostName = nodeInfo.host_name
            instDiskInfo = getNodeInstallationDiskInfo(nodeInfo.id)
            
            # installation disk details
            systemSpace = int(instDiskInfo.system_space * 1000)
            swapSize = 1048
            extraSize = int(instDiskInfo.storage_space * 1000)
            extraSize -= swapSize
            
            # pxe network details
            pxeInfo = PxeNetwork.objects.get()
            pxeIp = pxeInfo.ip 
            
            #Getting the password
            osPassword = getSystemPass()
            
            # encrypr password
            encryptPass = executeCommand("echo '" + osPassword + "' | openssl passwd -1 -stdin")
                    
            cobblerCmd = "cobbler system add --name=" + hostName + " --profile=" + settings.COBBLER_UBUNTU_PROFILE
            cobblerCmd += " --mac=" + netDeviceMac + " --hostname=" + hostName + " --interface=" + nicName
            cobblerCmd += " --kopts=\"netcfg/choose_interface=" + nicName + "\" --kickstart=/var/lib/cobbler/kickstarts/ubuntu1204-custom.preseed"
            cobblerCmd += " --ksmeta='interface=" + nicName + " drive=" + instDiskInfo.name + " syslabel=system extralabel=extra" 
            cobblerCmd += " syssize=" + str(systemSpace) + " swapsize=" + str(swapSize) + " extrasize=" + str(extraSize)
            cobblerCmd += " baseurl=" + pxeIp + ":8080  system=" + hostName + " rootpass=" + encryptPass + "'"
            cobblerCmd += "; cobbler sync"
            
            print "cobbler system add command:\n" + cobblerCmd
                        
            # if execute command success
            if executeCommand(cobblerCmd):
            
                # create chef command        
                chefCommand = getNodeChefDeploymentCommand(nodeInfo, envName, True) + " --run-list 'recipe[reboot::default]'"
                
                # execute the chef command
                try:
                    outputStr = executeChefCommand(chefCommand)
                    
                    # if error occured while deployment
                    if "Chef Client finished" in outputStr:
                        jobStatus = 'S'
                        print "\n\n" + outputStr + "\n\n"
                    else:
                        jobStatus = 'F'
                        errorMsg = findChefErrorMag(outputStr)
                    
                except Exception, e:
                    debugException(e)
                    jobStatus = 'F'
                    
                    # if attribute exists    
                    if hasattr(e, 'cmd'):
                        
                        # if IO error occured after reboot and chef reboot was success
                        if "Chef Client finished" in e.output:
                            jobStatus = 'S'
                        else:
                            errorMsg = "Command: " + e.cmd + " \nMessage: " + e.output
                    else:
                        errorMsg = "Error occured while installing os"
            else:
                jobStatus = 'F'
                errorMsg = "Error occured while cobbler system add"
                
        except Exception, e:
            debugException(e)
            jobStatus = 'F'
            errorMsg = "Error occured while cobbler system add"
        
        installStatus['jobStatus'] = jobStatus
        installStatus['errorMsg'] = errorMsg
            
    return installStatus


def deployRoleToNode(nodeInfo, recipePrList, jobId, roleCode):
    '''
    function to deploy role to a node
    nodeInfo        The node object
    recipePrList    Array contain recipie in priority lists
    jobId           The id of the job
    roleCode        The code of the role deployed to node
    '''
            
    jobStatus = 'S'
    progressEnd = len(recipePrList) + 3
    progressVal = 1

    from cloud.common import *
        
    # update cloud environment in chef server to override with dynamic values
    try:
        outputStr = updateDeploymentEnvironment(nodeInfo.cloud_id, nodeInfo, roleCode)
                 
        # if error exist in output
        if "ERROR:" in outputStr:
            jobStatus = 'F'
            errorMsg = outputStr
        else: 
         
            # update data bags
            try:
                outputStr = updateDeploymentDataBags(nodeInfo.cloud_id)
                 
                # if error exist in output
                if "ERROR:" in outputStr:
                    jobStatus = 'F'
                    errorMsg = outputStr
                 
            except Exception, e:
                jobStatus = 'F'
                debugException(e)
                 
                # if attribute exists    
                if hasattr(e, 'cmd'):
                    errorMsg = "Command: " + e.cmd + " \nMessage: " + e.output
                else:
                    errorMsg = "Error occured while updating chef data bags"
                 
         
    except Exception, e:
        jobStatus = 'F'
        debugException(e)
         
        # if attribute exists    
        if hasattr(e, 'cmd'):
            errorMsg = "Command: " + e.cmd + " \nMessage: " + e.output
        else:
            errorMsg = "Error occured while updating chef environment"
     
    # if it is object storage update the roles before deployment
    if (jobStatus == 'S') and (roleCode == 'object_storage' or roleCode == 'controller'):
         
        # update oject storage roles 
        try:
            outputStr = updateObjectStorageRole()
             
            # if error exist in output
            if "ERROR:" in outputStr:
                jobStatus = 'F'
                errorMsg = outputStr
                 
        except Exception, e:
            debugException(e)
            jobStatus = 'F'
         
            # if attribute exists    
            if hasattr(e, 'cmd'):
                errorMsg = "Command: " + e.cmd + " \nMessage: " + e.output
            else:
                errorMsg = "Error occured while updating chef roles of object storage"
    
             
    # if no error occured
    if jobStatus == 'S':
        
        # save job progress
        saveJobProgress(jobId, progressVal, progressEnd)
        
        # find environment name
        cloud = Cloud.objects.get(pk = nodeInfo.cloud_id)
        envName = generateEnvironmentName(cloud.cloud_name)
        outputStr = ''
        
        # check main os installation needed or not
        if not nodeInfo.currentos:
            installStatus = installOpenstackOS(nodeInfo, envName)
            
            # if success
            if installStatus['jobStatus'] == 'S':    
                nodeInfo.currentos = True
                nodeInfo.node_up = False
                nodeInfo.save()
                saveJobProgress(jobId, progressVal + 1, progressEnd)
                msgTxt = "Started main os installation"
                saveJobNodeLog(jobId, nodeInfo, msgTxt, msgTxt, True)
                return {'status': 'Success', 'successMsg': msgTxt}
            else:
                jobStatus = installStatus['jobStatus']
                errorMsg = installStatus['errorMsg']
        
        # prepare node for installation
        if jobStatus == 'S':
            preparedStatus = prepareNode(nodeInfo, envName)
            jobStatus = preparedStatus['jobStatus']
            errorMsg = preparedStatus['errorMsg']
        
        # if no error occured
        if jobStatus == 'S':
            
            # save job progress
            saveJobProgress(jobId, progressVal + 2, progressEnd)
            
            # loop through the priority list of recipies for role to execute it first
            for priority, recipeList in recipePrList.iteritems():
            
                recipeNameList = ""
                errorMsg = ''
                
                # loop through recipe list and create recipe name list
                for recipe in recipeList:
                    
                    # more than one recipe name
                    if "recipe[" in recipe.recipe_name:
                        recipeNameList += recipe.recipe_name + ","
                    else:
                        recipeNameList += "recipe[" + recipe.recipe_name + "],"
                
                # if object storage related deployment in controller, just skip it
                # anyway we are deploying it later through object storage role
                if 'openstack-object-storage::setup' in recipeNameList:
                    continue 
                elif 'role[os-object-storage-account]' in recipeNameList:
                    outputStr = deployObjectStorage(nodeInfo, roleCode, envName)
                else:
                    
                    # create chef command using the recipe name list
                    recipeNameList = re.sub(r",$", "", recipeNameList)
                    chefCommand = getNodeChefDeploymentCommand(nodeInfo, envName) + " --run-list '" + recipeNameList + "'"
                    
                    # execute the chef command
                    try:
                        outputStr = executeChefCommand(chefCommand)
                    except Exception, e:
                        debugException(e)
                        jobStatus = 'F'
                        errorMsg = "Command: " + e.cmd + " \nMessage: " + e.output
                        break
                    
                # if error occured while deployment
                if "Chef Client finished" in outputStr:
                    jobStatus = 'S'
                    print "\n\n" + outputStr + "\n\n" 
                    
                    # save job progress
                    progressVal = progressVal + 1
                    saveJobProgress(jobId, progressVal, progressEnd)
                    
                else:
                    jobStatus = 'F'
                    
                    # if particular error message in string
                    if errorMsg.__eq__(''):
                        errorMsg = findChefErrorMag(outputStr)
                    
                    break
    
    # save job status
    saveJobStatus(jobId, jobStatus)
    
     # if job is success
    if jobStatus == 'S':
        logTitle = "Successfully deployed role[" + roleCode + "] in node: " + nodeInfo.node_ip 
        logMessage = outputStr
        returnInfo = {'status': 'Success', 'successMsg': logTitle}
        logStatus = True
        saveJobProgress(jobId, progressEnd, progressEnd)
        
    else:
        logTitle = "Deployment of role[" + roleCode + "] in node: " + nodeInfo.node_ip + " failed!"
        logMessage = errorMsg
        returnInfo = {'status': 'Error', 'errorMsg': errorMsg}
        logStatus = False
    
    # check whether cloud deployment completed
    if isCloudDeploymentComplete(nodeInfo.cloud_id):
        
        jobList = Job.objects.filter(cloud_id = nodeInfo.cloud_id, job_status = "F")
        cloudnfo = Cloud.objects.get(id = nodeInfo.cloud_id)
        
        # if jobs failed
        if len(jobList):
            params = {
                'alert_type': 'Cloud',
                'referece_id': nodeInfo.cloud_id,
                'alert_content': "Deployment of '" + cloudnfo.cloud_name + "' failed!",
                'alert_status' : 'F'
            }
        else:
            dashboardLink = getCloudDashBoardLink(nodeInfo.cloud_id, 'P')
            
            # if empty public link show local link
            if not dashboardLink:
                dashboardLink = getCloudDashBoardLink(nodeInfo.cloud_id, 'M')
            
            message = "'" + cloudnfo.cloud_name + "' deployed successfully in <a href='" + dashboardLink + "'>" + dashboardLink + "</a>"
            params = {
                'alert_type': 'Cloud', 
                'referece_id': nodeInfo.cloud_id,
                'alert_content': message,
                'alert_status' : 'S'
            }
            
        # calling the function to add the alert
        thunderAlertAdd(params, True)
    
    # save nod log status
    saveJobNodeLog(jobId, nodeInfo, logTitle, logMessage, logStatus)
    
    return returnInfo

def findChefErrorMag(outputStr):
    '''
    function to find chef error message
    outputStr -  the chef command output string
    @return -  errorMsg - The error message found
    '''
    
    # check for the error formats
    if "Running handlers:" in outputStr:
        errorMsg = outputStr.split("Running handlers:", 1)[1]
    elif "ERROR:" in outputStr:
        errorMsg = outputStr.split("ERROR:", 1)[1] 
    else:
        errorMsg = outputStr
    
    return errorMsg


def getNodeChefDeploymentCommand(nodeInfo, envName = '', chefInstall = False):
    '''
    function to get node chef command
    nodeInfo - The node information object
    envName - The environment name
    chefInstall - Install chef client or not
    @return chefCommand  The prepared chefcommand
    '''
    
    chefCommand = "knife bootstrap " + nodeInfo.node_ip + " --ssh-user " + nodeInfo.user_name
    chefCommand += " --ssh-password '" + nodeInfo.password + "' --sudo --use-sudo-password"
    chefCommand += " --node-name node" + str(nodeInfo.id)
    
    # if environment name is passed
    if envName != '':
        chefCommand += " --environment " + envName
        
    # if prepare node option set bootstrp install command
    if chefInstall:
        chefPkgName = 'chef_11.18.6-1_amd64.deb'
        downloadLink = settings.PKG_DOWNLOAD_URL + "/" + chefPkgName
	etcHostUpdateEntry = 'echo "' + settings.CHEF_SERVER_IP + ' thunder" >> /etc/hosts;'
        chefCommand += " --bootstrap-install-command '" + etcHostUpdateEntry + "type chef-client >/dev/null 2>&1 || { wget " + downloadLink + "; dpkg -i " + chefPkgName + "; rm -f /etc/chef/client.pem;}'"
    
    return chefCommand

def getLocalmodeChefDeploymentCommand():
    '''
    function to get node chef command
    @return chefCommand  The prepared chefcommand
    '''
    
    chefCommand = "chef-client --local-mode --runlist"
    return chefCommand


def getLocalChefServerDeploymentCommand(nodeName = 'thunder', envName = ''):
    '''
    function to get node chef command
    envName - The environment name
    @return chefCommand  The prepared chefcommand
    '''
   
    from cloud.common import * 
    chefCommand = "chef-client --node-name " + nodeName + " --config " + CHEF_REPO_DIR + "/.chef/client.rb"
    chefCommand += " --validation_key " + CHEF_REPO_DIR + "/.chef/aqorn-validator.pem"
    
    # if environment name is passed
    if envName != '':
        chefCommand += " --environment " + envName
    
    return chefCommand
    

def prepareNode(nodeInfo, envName):
    '''
    function to prepare node
    nodeInfo - The node information object
    envName         the name of the chef environment
    @return prepareStatus  The prepared status of node
    '''
    
    prepareStatus = {}
    prepareStatus['jobStatus'] = 'S'
    prepareStatus['errorMsg'] = ''
    errorMsg = ''
    
    # if node is not prepared
    if not nodeInfo.prepared:
        
        # create chef command
        chefCommand = getNodeChefDeploymentCommand(nodeInfo, envName, True) + " --run-list 'recipe[thunder-setup::prepare_node]'"
        
        # execute the chef command
        try:
            outputStr = executeChefCommand(chefCommand)
            
            # if error occured while deployment
            if "Chef Client finished" in outputStr:
                jobStatus = 'S'
                print "\n\n" + outputStr + "\n\n"
                
                # save node prepared value    
                nodeInfo.prepared = True
                nodeInfo.save()
            else:
                jobStatus = 'F'
                errorMsg = findChefErrorMag(outputStr)
            
        except Exception, e:
            debugException(e)
            jobStatus = 'F'
            
            # if attribute exists    
            if hasattr(e, 'cmd'):
                errorMsg = "Command: " + e.cmd + " \nMessage: " + e.output
            else:
                errorMsg = "Error occured while preparing nodes"
        
        prepareStatus['jobStatus'] = jobStatus
        prepareStatus['errorMsg'] = errorMsg
            
    return prepareStatus 


def deployRevokeNodeRole(nodeInfo, jobId, roleCode):
    '''
    function to revoke a role from a node
    nodeInfo        The node object
    jobId           The id of the job
    roleCode        The code of the role deployed to node
    '''
    
    # find environment name
    cloud = Cloud.objects.get(pk = nodeInfo.cloud_id)
    envName = generateEnvironmentName(cloud.cloud_name)
    
    # create chef command using the recipe name list
    jobStatus = 'S'
    recipeName = 'recipe[thunder-setup::' + roleCode + '_revoke]'
    chefCommand = getNodeChefDeploymentCommand(nodeInfo, envName) + " --run-list '" + recipeName + "'"
    
    # execute the chef command
    try:
        outputStr = executeChefCommand(chefCommand)
        
        # if error occured while deployment
        if "Chef Client finished" in outputStr:
            jobStatus = 'S'
            print "\n\n" + outputStr + "\n\n" 
        else:
            jobStatus = 'F'
            
            # if particular error message in string
            if errorMsg.__eq__(''):
                errorMsg = findChefErrorMag(outputStr)
        
    except Exception, e:
        debugException(e)
        jobStatus = 'F'
        
        # if attribute exists    
        if hasattr(e, 'cmd'):
            errorMsg = "Command: " + e.cmd + " \nMessage: " + e.output
        else:
            errorMsg = "Error occured while revoking role"
        
    # save job status
    saveJobStatus(jobId, jobStatus)
    
     # if job is success
    if jobStatus == 'S':
        logTitle = "Successfully revoked role[" + roleCode + "] in node: " + nodeInfo.node_ip 
        logMessage = outputStr
        returnInfo = {'status': 'Success', 'successMsg': logTitle}
        logStatus = True 
    else:
        logTitle = "Revoking role[" + roleCode + "] in node: " + nodeInfo.node_ip + " failed!"
        logMessage = errorMsg
        returnInfo = {'status': 'Error', 'errorMsg': errorMsg}
        logStatus = False
    
    # save nod log status
    saveJobNodeLog(jobId, nodeInfo, logTitle, logMessage, logStatus)
    
    # check whether cloud deployment completed
    if isCloudDeploymentComplete(nodeInfo.cloud_id):
        jobList = Job.objects.filter(cloud_id = nodeInfo.cloud_id, job_status = "F")
        
        # if all jobs are success
        if len(jobList) == 0:
            doDeleteCloud(nodeInfo.cloud_id)
    
    return returnInfo


def doDeleteCloud(cloudId):
    '''
    function to delete cloud
    cloudId - cloud id
    '''

    # delete cloud
    try:
        
        # get zabbix host id
        nodeList = Nodelist.objects.filter(cloud_id = cloudId)
        zabbixHostList = []
        
        # loop through nod elist
        for nodeInfo in nodeList:
            zabbixHostList.append(nodeInfo.zabbix_host_id)
        
        # delete all zabbix hosts
        zabbixHostDelete(zabbixHostList)
        
        # delete all nodes of cloud
        Nodelist.objects.filter(cloud_id = cloudId).delete()
        
        # To delete the domains / users associated with the cloud
        domainFilterList = CloudDomainMap.objects.filter(cloud = Cloud(cloudId)).distinct()
        
        # Create the domain list
        domainList = []
        for domain in domainFilterList:
            domainList.append(int(domain.domain_id))
        
        # delete cloud
        cloudnfo = Cloud.objects.get(id = nodeInfo.cloud_id)
        cloudName = cloudnfo['cloud_name']
        cloudnfo.delete()
        
        # Delete cloud domains of the cloud
        CloudDomain.objects.filter(id__in = domainList).delete()

        # To delete the users that are not associated with any roles / domain
        cursor = connection.cursor()
        userIds = []

        #sql for the data selection
        sql = "select user.id from auth_user user,thunder_user_role_mapping user_map where user_map.user_id != user.id;"
        cursor.execute(sql)
        userIdList = cursor.fetchall()

        # Create user list
        for id in userIdList:
            
            #Checking the the user id is not equal to logged in user. This is to prevent deletion of logged in user.
            #if int(id[0]) != request.user.id:
            userIds.append(int(id[0]))

        # Deletes the users related to the roles / domain
        #User.objects.filter(id__in = userIds).delete()
        
        #To show the alerts
        params = {
            'alert_type': 'Cloud',
            'referece_id': nodeInfo.cloud_id,
            'alert_content': "Cloud " + cloudName + " deleted successfully",
            'alert_status' : 'S'
        }
        
        thunderAlertAdd(params)
        return True
        
    except Exception, e:
        debugException(e)
        return False;
    

def  deployObjectStorage(nodeInfo, roleCode, envName):
    '''
    function to execute chef command from chef-repo
    nodeInfo        The node object
    roleCode        The code of the role deployed to node
    envName         the name of the chef environment
    @return outputStr  the output of the execution
    ''' 
    
    # find object storage nodes assigned and controller IP
    cloudId = nodeInfo.cloud_id
    controllerIPList = getAllControllers(cloudId)
        
    # if controller node list is empty
    if not controllerIPList:
        return "Error: Controller node not found"
    
    # get al object storage nodes
    obStorageList = getAllObjectStorageNode(cloudId)         
    
    # if object storage list is empty return error
    if not obStorageList:
        
        # if controller just skip the installation and wait for storage assignment
        if roleCode == "controller":
            return "Chef Client finished: Skipping installation due to no object storage nodes found"
        else:
            return "Error: Please add atleast 1 object storage node to deploy swift proxy server!"
        
    else:
        controllerRecipe = getObjectStorageRecipeName('controller')
        obStorageRecipe = getObjectStorageRecipeName('object_storage')
        swiftStorageNodeList = []
        chefCommandList = []
        obCmdList = []
    
        # loop through storage node list
        for storageNodeId in obStorageList:
            swiftStorageNodeList.append(Nodelist.objects.get(pk = storageNodeId[0]))
            
        # loop through storage node and execute
        for swiftStorageNodeInfo in swiftStorageNodeList:
            
            # prepare node for installation
            preparedStatus = prepareNode(swiftStorageNodeInfo, envName)
            
            # if prepare failed
            if preparedStatus['jobStatus'] == 'F':
                return "Error: " + preparedStatus['errorMsg']
            
            swiftStorageChefCmd = getNodeChefDeploymentCommand(swiftStorageNodeInfo, envName) + " --run-list '" + obStorageRecipe + "'"
            obCmdList.append(swiftStorageChefCmd)
            chefCommandList.append(swiftStorageChefCmd)
        
        # execute in controller node
        for ipInfo in controllerIPList:
            controllerNodeInfo = Nodelist.objects.get(pk = ipInfo['id'])
            swiftControllerChefCmd = getNodeChefDeploymentCommand(controllerNodeInfo, envName) + " --run-list '" + controllerRecipe + "'"
            chefCommandList.append(swiftControllerChefCmd)
        
        # append all chef commands
        chefCommandList = chefCommandList + obCmdList
    
    # execute chef commands
    for chefCommand in chefCommandList:
    
        # execute the chef command
        try:
            outputStr = executeChefCommand(chefCommand)
            
            # if error occured while deployment
            if "Chef Client finished" in outputStr:
                print "\n\n" + outputStr + "\n\n" 
            else:
                return "Error: " + findChefErrorMag(outputStr) 
            
        except Exception, e:
            debugException(e)
            return "Error: Command: " + e.cmd + " \nMessage: " + e.output
    
    
    return "Chef Client finished: Success"
    

def getObjectStorageRecipeName(roleCode):
    '''
    function to get recipe name
    roleCode        The code of the role deployed to node
    @return recipeName        The name of recipe 
    '''

    role = Roletype.objects.get(role_code = roleCode)
    
    try:
        
        # if controller role
        if roleCode == 'controller':
            recipeInfo = Recipe.objects.filter(
                roletype_id = role.id, recipe_name__contains='openstack-object-storage::setup', status =1
            ).first()
        else:
            recipeInfo = Recipe.objects.filter(
                roletype_id = role.id, status =1
            ).first()
        
        recipeName = recipeInfo.recipe_name
        
    except Exception, e:
        debugException(e)
        recipeName = ''
    
    return recipeName

    
def getAllObjectStorageNode(cloudId):
    '''
    function to get all object storage node
    cloudId  - The id of the cloud
    @return obStorageList - The list contains object storage node list
    ''' 
    
    obStorageList = []
    sql = "select nl.id from thunder_nodelist nl, thunder_noderole nr, thunder_roletype role"
    sql += " where nl.id=nr.node_id and nr.role_id=role.id and role.role_code='object_storage'"
    sql += " and nl.status=1 and cloud_id=" + str(cloudId)
    
    # use cursor to get the controller assigned IP
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        obStorageList = cursor.fetchall()
        
    except Exception, e:
        debugException(e)
    
        # if attribute exists    
        if hasattr(e, '__cause__'):
            print e.__cause__
        else:
            print "Internal error occured while finding controller IP"
    
    return obStorageList   


def executeChefCommand(chefCommand, shellFlag = True):
    '''
    function to execute chef command from chef-repo
    chefCommand - Command to execute in chef chef repo
    shellFlag - execute in shell or not[default - True]
    Return - outputStr output of the command
    '''
    
    # print chef command
    print "\n" + chefCommand + "\n"
   
    from cloud.common import * 
    os.chdir(CHEF_REPO_DIR)
    outputStr = subprocess.check_output(chefCommand, shell = shellFlag)
    os.chdir(settings.THUNDER_ABS_PATH)
    
    return outputStr


def executeCommand(command, shellFlag = True, debug = False):
    '''
    function to execute chef command
    command - Command to execute
    shellFlag - execute in shell or not[default - True]
    debug -The debug option
    Return - outputStr output of the command
    '''
            
    # execute comamnd
    try:
        outputStr = subprocess.check_output(command, shell = shellFlag)
    except Exception, e:
        debugException(e)
        outputStr = ""
        
        # if debug print commands
        if debug:
            print "\nCommand: " + command + "\n"
            print "\nException: "
            print e
            print "\n"
    
    return outputStr


def parseChefResult(outputStr): 
    '''
    function to parse the output result content
    outputStr - The output string to be parsed
    @return The parsed string
    '''
    
    # do regex search
    try:
        match = re.search(r'==TH_HEAD_RES==(.*?)==TH_FOOT_RES==', outputStr, re.DOTALL)
        return str(match.group(1))
    except Exception, e:
        debugException(e)
        return ""

def parseChefSubResult(outputStr, tagName): 
    '''
    function to parse the output result content
    outputStr - The output string to be parsed
    tagName - The name of the tag
    @return The parsed string
    '''
    
    # do regex search
    try:
        match = re.search(r'@@' + tagName + '@@(.*?)@@' + tagName + '@@', outputStr, re.DOTALL)
        return str(match.group(1))
    except Exception, e:
        debugException(e)
        return ""
    

def getCloudOptions(cloudId):
    '''
    function to get cloud option values with overrided values saved
    cloudId -     The id of the cloud
    @return overrideValList The option value dict
    '''
    
    # get all options available for thunder  
    overrideValList = {}  
    optColListList = ThunderOption.objects.all()
    
    # loop through option column 
    for optVal in optColListList:
        overrideValList[optVal.id] = optVal.default_value
    
    # get all options saved for cloud
    optionValList = ThunderOptionValue.objects.filter(cloud_id = cloudId)
    
    # loop through it to override default value list
    for optVal in optionValList:
        overrideValList[optVal.option_id] = optVal.option_value
        
    return overrideValList

def saveJobStatus(jobId, jobStatus):
    '''
    function to save job status
    jobId     - The id of the job
    jobStatus - The status of job[N/P/F/S]
    '''
    
    # store results in job and nodelog
    job = Job.objects.get(pk = jobId)
    job.job_status = jobStatus
    job.end_time = datetime.datetime.now()
    job.save()    
    
    
def saveJobProgress(jobId, progressVal, progressEnd):
    '''
    function to save job progress
    jobId     - The id of the job
    progressVal - The value of progress
    progressEnd - The value for end
    '''
    
    # store results in job and nodelog
    job = Job.objects.get(pk = jobId)
    progressEnd = float(progressEnd)
    progressVal = float(progressVal)
    progressVal = (progressVal / progressEnd) * 100
    progressVal = round(progressVal)
    job.job_progress = 100 if progressVal > 100 else progressVal
    job.end_time = datetime.datetime.now()
    job.save()
    
    
def saveJobNodeLog(jobId, nodeInfo, logTitle, logMessage, logStatus, logType = 'JOB'):
    '''
    function to save the job log details in node log table
    jobId     - The id of the job
    nodeInfo  -    The object of node
    logTitle  -    The title of the log
    logMessage -   The details of the log message
    logStatus -    The status of the log[True/False]
    logType  -     The type of the job
    '''
    
    # save node log details for a job
    nodelog = Nodelog(
        node_listid = nodeInfo.id, subject_id = jobId, log_type = logType,
        log_title = logTitle, log_details = logMessage, status = logStatus
    )
    nodelog.save()
    
    
def isCloudDeploymentComplete(cloudId):
    """
    function to check whether cloud deployment in Progress
    cloudid - The id of the cloud
    @return - True / False   Completed / In progress
    """
    
    # check status of jobs
    try:
        
        jobList = Job.objects.filter(cloud_id = cloudId, job_status__in = ["N", "P"])
        return False if len(jobList) > 0 else True
        
    except Exception, e:
        debugException(e)
        return False
    
    
def getCloudDashBoardLink(cloudId, netType):
    """
    function to get dashboard Link
    cloudid - The id of the Cloud
    """
    
    dashboardLink = ""
    from deployment.environment import *
    controllerIPList = getAllControllers(cloudId, netType)
    
    # if controller ip list is not empty
    if len(controllerIPList):
        
        # loop through the list
        for controllerIPInfo in controllerIPList:
            
            # if controller ip is not empty
            if controllerIPInfo['ip']:
                dashboardLink = "http://" + controllerIPInfo['ip'] + "/"
                break
        
    return dashboardLink


def getCloudRoleList():
    """
    function to get cloud role list
    """
    
    roleList = {}

    # get all available roles
    try:
        list = Roletype.objects.all()
        
        # loop through list
        for listInfo in list:
            roleList[listInfo.id] = listInfo
        
    except Exception, e:
        debugException(e)
    
    return roleList    
        
