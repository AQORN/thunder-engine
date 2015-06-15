# @author: Binoy
# @create_date: 5-May-2015
# @modified by: Binoy    
# @modified_date: 5-May-2015
# @linking to other page: 
# @description: Common system functions
from django.db.models import Q
from django.conf import settings
from thunderadmin.models import *
from cloud.models import *
from django.contrib import messages
from deployment.common import *
from network.functions import *
import subprocess

def checkAdminUpdated():
    """
    To check the admin is updated correctly
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns  response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    status = InstallationStatus.objects.filter(Q(status = 0))
    return len(status)

def checkInstallationStatus():
    """
        To check whether the components are installed and get the status
    """

    try:

        # Fetch the installation status
        installationStatus = InstallationStatus.objects.filter(name = 'Installation Status')
        installationStatus = installationStatus[0]

        # Checks if it is complete
        if installationStatus.state == 'S':
            return True
        else:
            return False

    except Exception, e:

        print e
        return False

def adminSetupDetails():
    """To show the list of roles assinged
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    
    #Getting the details from the tables
    thunderVersions = PatchUpdate.objects.all().order_by('-intsalled_on')[:1]
    pxeNetworks = PxeNetwork.objects.all()
    thunderAcces = ThunderAcces.objects.all()
    
    #Setting the values for the template
    pxeList = []
    version = 'UNDEFINED'
    thunderLink = 'UNDEFINED'
    
    #Getting the thunder version
    for thunderVersion in thunderVersions:
        version = thunderVersion.version
        
    #Getting the thunder access
    for thunder in thunderAcces:
        thunderLink = thunder.ip_address
    
    #Looping through the values
    if len(pxeNetworks):
        for pxeNetwork in pxeNetworks:
            pxeData = {}
            pxeData['pool_start'] = pxeNetwork.pool_start
            pxeData['pool_end'] = pxeNetwork.pool_end
            pxeData['subnet_mask'] = pxeNetwork.subnet_mask
            pxeData['gateway'] = pxeNetwork.gateway
            pxeData['nic_name'] = pxeNetwork.nic.name
            pxeData['thunder_version'] = version
            pxeData['thunder_access'] = thunderLink
            pxeList.append(pxeData)
            pxeNetwork.gateway
    else:
        pxeData = {}
        pxeData['pool_start'] = 'UNDEFINED'
        pxeData['pool_end'] = 'UNDEFINED'
        pxeData['subnet_mask'] = 'UNDEFINED'
        pxeData['gateway'] = 'UNDEFINED'
        pxeData['nic_name'] = 'UNDEFINED'
        pxeData['thunder_version'] = version
        pxeData['thunder_access'] = thunderLink
        pxeList.append(pxeData)
   
    #returning the response to the html
    return {'pxeNetworks': pxeList}

def chkPxeUpdated():
    """To check the pxe details is updated
    Returns:
        Returns update status
        
    Raises:
        Exceptions and redirection to the login page.
    """
    status = InstallationStatus.objects.get(id = 1)
    
    #returning the status
    return status

def chkThunderAccessUpdated():
    """To check the thunder access is updated
    Returns:
        Returns update status

    Raises:
        Exceptions and redirection to the login page.
    """

    # Get the installation status for thunder access
    status = InstallationStatus.objects.get(id = 2)

    # returning the status
    return status

def deleteCloudAdmin(request):
    """
    To delete the node role, jobs etc
    Args:
        {
            request - null
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.     
    """ 
    
    # getting the node list from the table
    nodeLists = Nodelist.objects.all()
    
    #looping through the list
    for nodeList in nodeLists:
        
        #Getting the related node roles
        nodeRoles = NodeRole.objects.filter(node_id = nodeList.id)
        
        #looping through the roles
        for nodeRole in nodeRoles:
            
            #Getting the related jobs
            jobs = Job.objects.filter(subject_id = nodeRole.id)
            
            #If jobs are listed then adding the revoke 
            if len(jobs) != 0:
                
                #loopign through the jobs
                for job in jobs:
                    
                    #if the job is new and role type is assign then deleting job and related roles 
                    if job.job_status == 'N' and job.job_type == 'ROLE_ASSIGN' :
                        Job.objects.get(pk = job.id).delete()
                        NodeRole.objects.filter(pk = nodeRole.id).delete()
                        messages.add_message(request, messages.SUCCESS, 'Node role and job is deleted.')
                    else:
                        jobStatus = Job.objects.get_or_create(cloud_id = nodeList.cloud_id, job_type = 'ROLE_REVOKE', subject_id = nodeRole.id, job_status= 'N')
                        
                        #to show the message to the user.
                        if jobStatus[1] == True:
                            messages.add_message(request, messages.SUCCESS, 'Revoke Job Added to the queue successfully.')
                        else:
                            messages.add_message(request, messages.ERROR, 'Revoke Job already exsists.')
            else:
                
                #deleting the node role.
                NodeRole.objects.filter(pk = nodeRole.id).delete()
                messages.add_message(request, messages.SUCCESS, 'Since there is no job, job role also deleted.')


def executeServiceInstallation(service):
    """
        Function to execute the service installation
    """

    # Initialising the data variable
    responseData = {}
    status = True

    # Create local node chef command
    chefCommand = getLocalmodeChefDeploymentCommand() + " 'recipe[thunder-install::install_" + service + "]'"

    # execute the chef command
    try:
        outputStr = executeChefCommand(chefCommand)

        # if error occurred while deployment
        if "Chef Run complete" not in outputStr:
            status = False

    except Exception, e:

        # Setting the response data
        responseData['error'] = str(e)
        status = False
        error = ""

        # if attribute exists
        if hasattr(e, 'cmd'):
            error = "Command: " + e.cmd + " \nMessage: " + e.output
        else:
            error = "Error occured while executing " + service + " installation"

        # Display error
        debugException(error)

    # Setting the response data
    responseData['error'] = "Error occured while executing " + service + " installation"
    responseData['status'] = status

    return responseData

def getServiceDetails(services):
    """
        Function to check the service status
    """
    
    #Getting the service status
    try:
        #Running the command and getting the result from it
        processDetails = subprocess.check_output(services, shell = True).splitlines()
        return processDetails
    except subprocess.CalledProcessError as e:
        return 'down'
    
def executeServiceCommnd(services):
    """
        Function to execute the service status
    """
    
    # Create local node chef command
    chefCommand = getLocalmodeChefDeploymentCommand() + " 'recipe[thunder-common::" + services +"]'"
    
    # execute the chef command
    try:
        outputStr = executeChefCommand(chefCommand)

        # if error occurred while deployment
        if "Chef Run complete" not in outputStr:
            return False
        else:
            return True

    except Exception, e:

        # if attribute exists
        if hasattr(e, 'cmd'):
            debugException("Command: " + e.cmd + " \nMessage: " + e.output)
        else:
            debugException("Error occured while executing " + services + " installation")

        return False
    
    

def getLocalNodeInformation():
    '''
        Function to fetch the node information
        @return  : node info
    '''

    # Create local node chef command
    chefCommand = getLocalmodeChefDeploymentCommand() + " 'recipe[thunder-common::get_node_details]'"

    # execute the chef command
    try:
        outputStr = executeChefCommand(chefCommand)

        # if error occurred while deployment
        if "Chef Run complete" not in outputStr:
            return False

    except Exception, e:

        # if attribute exists
        if hasattr(e, 'cmd'):
            debugException("Command: " + e.cmd + " \nMessage: " + e.output)
        else:
            debugException("Error occured while fetching node information")
        return False

    # parse chef results
    nodeContent = parseChefResult(outputStr)

    # save network details
    networkContent = parseChefSubResult(nodeContent, "NIC_RES")

    # convert to string and find values
    networkContent = str(networkContent).replace("=>", ":")

    # check json can be parsed
    try:
        networkInfo = json.loads(networkContent)
    except Exception, e:
        debugException(e)
        return False

    # Setting the default nic
    defaultNic = networkInfo['default_interface'] if networkInfo.has_key('default_interface') else ""
    nicList = []

    # check whether network info details present
    if networkInfo and networkInfo.has_key('interfaces'):

        # loop through the network info
        for nicName, nicInfo in networkInfo['interfaces'].items():

            # Initialse the data variable to set nic info
            newNICInfo = {}

            # if nicname not loopback address
            if nicName not in ['lo'] and "LOOPBACK" not in nicInfo['flags']:

                # Set nic info
                newNICInfo["name"] = str(nicName)
                macAddress = ""

                # loop through nic info details
                for nKey, nVal in nicInfo['addresses'].items():

                    # find mac address
                    if nVal.has_key("family") and not nVal.has_key("prefixlen"):

                        # set macaddr
                        macAddress = str(nKey)
                        newNICInfo["macAddress"] = str(macAddress)

                # Sets the niclist with new data
                nicList.append(newNICInfo)

    return nicList

def saveNics(nicList):
    """
        Function to save the network card details to db
    """

    # Initialising the data variable
    status = True

    # Loops through the list and save the info in thunder db
    for nic in nicList:

        try:

            # Create the new nic entry
            NetworkCard.objects.get_or_create(name = nic['name'], mac_address = nic['macAddress'])
        except Exception, e:

            # Sets the status
            print e
            status = False

    return status

def installationDataSetUP(fileTemplate, setUpData, destFile):
    """
        Function to handle the thunder installation on opting to apply
        the changes with data set in admin console.
    """

    # Setting the initial data values
    status = True
    srcData = ""
    srcFileLoc = settings.THUNDER_ABS_PATH + "/cloud/templates/thunderadmin/sources/"
    templateSrcLoc = srcFileLoc + fileTemplate + ".src"

    try:

        # Get the src template contents, read it and save.
        templateSrc = open(templateSrcLoc)
        srcData = templateSrc.read()

        # Replace the data passed in the template content.
        for placeholder, dataValue in setUpData.iteritems():
            srcData = srcData.replace("{{" + placeholder + "}}", dataValue)

        # Write out the modified content into the destination file.
        destFileLoc = open(destFile, "w")
        destFileLoc.write(srcData)
    except Exception, e:

        # Sets the return status value
        print "Exception : ", e
        status = False

    return status

def setPasswordLock(request):
    """
    Function to lock the thunder with new passwrod
    """
    usr = User.objects.get(pk = 1)
    usr.set_password(settings.PASS_PREFIX + request.POST.get('password') + settings.PASS_SUFFIX)
    usr.save()

def executeBackEndSetUp():
    """
        Function to execute the post config submission setup for system services
    """
    
    # Initialise data variable
    responseData = {}
    status = True
    errMsg = ""
    networkTypeList = ["pxe", "install"]

    ### Set the data in chef attribute file ###

    # Fetch pxe config data and set to the template place holders
    pxeObj = PxeNetwork.objects.get(pk = 1)
    fromIp = pxeObj.pool_start
    toIp = pxeObj.pool_end
    pxeNetMask = pxeObj.subnet_mask
    pxeGateway = pxeObj.gateway
    pxeNicId = pxeObj.nic_id
    pxeSubnet = pxeObj.subnet
    pxeIp = pxeObj.ip

    # Get nic details for pxe
    pxeNicDetails = NetworkCard.objects.get(pk = pxeNicId)
    pxeNicName = pxeNicDetails.name
    
    # Fetch thunder access config data and set to the template place holders
    thunderAccessObj = ThunderAcces.objects.get(pk = 1)
    thunderNetmask = thunderAccessObj.subnet_mask
    thunderGateway = thunderAccessObj.gateway
    thunderNicId = thunderAccessObj.nic_id
    thunderIp = thunderAccessObj.ip_address
    thunderDns = thunderAccessObj.dns_ip

    # Get nic details for thunder access
    thunderNicDetails = NetworkCard.objects.get(pk = thunderNicId)
    thunderNic = thunderNicDetails.name
    
    ### Sets the attribute values and calls the chef recipe to make network change ###

    # Loop through the network types and set the network changes using chef command
    for networkType in networkTypeList:

        # Calls the function to save the data to chef attribute file
        installationDataSetUP("default.rb", {"pxe_gateway" : pxeGateway,
                                            "pxe_netmask" : pxeNetMask,
                                            "pxe_nic" : pxeNicName,
                                            "pxe_pool_start" : fromIp,
                                            "pxe_pool_end" : toIp,
                                            "pxe_subnet" : pxeSubnet,
                                            "pxe_ip" : pxeIp,
                                            "thunder_netmask" : thunderNetmask,
                                            "thunder_gateway" : thunderGateway,
                                            "thunder_nic" : thunderNic,
                                            "thunder_ip" : thunderIp,
                                            "thunder_dns" : thunderDns,
                                            "network_type" : networkType},
                                "/opt/thunder_web/chef-repo/cookbooks/thunder-install/attributes/default.rb")

        # Calls the chef command to set the network
        try:
            
            # Create local node chef command
            chefCommand = getLocalmodeChefDeploymentCommand() + " 'recipe[thunder-install::network_change]'"

            # execute the chef command
            outputStr = executeChefCommand(chefCommand)

            # if error occurred while deployment
            if "Chef Run complete" not in outputStr:
                status = False
                errMsg = "Error while setting the network interface details for %s" % (networkType)

        except Exception, e:
            
            # Sets the error details
            print e
            status = False
            errMsg = "Error while setting the network interface details for %s" % (networkType)

            # if attribute exists
            if hasattr(e, 'cmd'):
                errMsg = errMsg + "\nCommand: " + e.cmd + " \nMessage: " + e.output
            else:
                errMsg = errMsg + "\nError occured while modifying network"

            # Display Error
            debugException(errMsg)

        # Sets error details in response data and return them
        if status == False:
            responseData['status'] = status
            responseData['errMsg'] = "Error while setting the network interface details for %s" % (networkType)

            return responseData

    # Executes the service restarting recipe
    try:

        # Create local node chef command
        chefCommand = getLocalmodeChefDeploymentCommand() + " 'recipe[thunder-install::restart_services]'"

        # execute the chef command
        outputStr = executeChefCommand(chefCommand)

        # if error occurred while deployment
        if "Chef Run complete" not in outputStr:
            status = False
            errMsg = "Error while restarting the system services"

    except Exception, e:

        # Sets the error details
        print e
        status = False
        errMsg = "Error while restarting the system services"

        # if attribute exists
        if hasattr(e, 'cmd'):
            errMsg = errMsg + "\nCommand: " + e.cmd + " \nMessage: " + e.output
        else:
            errMsg = errMsg + "\nError occured while restarting system services"

        # Display Error
        debugException(errMsg)

        # Sets error details in response data and return them
        if status == False:
            responseData['status'] = status
            responseData['errMsg'] = "Error while restarting the system services"

            return responseData

    # Set the return data
    responseData['status'] = status

#     if status:
#         return HttpResponseRedirect(settings.BASE_URL)

    return responseData


def changeThunderIpSettings(thunderIp, pxeIp):
    '''
    function to set thunder ip and pxe ip in thunder settings file
    thunderIp - The ip of the thunder
    pxeIp - The ip of the pxe
    '''

    replaceFileLine(
        "THUNDER_HOST.*?=.*",
        'THUNDER_HOST = "' + thunderIp + '"',
        "/opt/thunder_web/thunder/settings.py"
    )
    replaceFileLine(
        "CHEF_SERVER_IP.*?=.*",
        'CHEF_SERVER_IP = "' + pxeIp + '"',
        "/opt/thunder_web/thunder/settings.py"
    )
    replaceFileLine(
        "LOCAL_REPO_IP.*?=.*",
        'LOCAL_REPO_IP = "' + pxeIp + ':8080"',
        "/opt/thunder_web/thunder/settings.py"
    )
    replaceFileLine(
        "ZABBIX_SERVER.*?=.*", 
        'ZABBIX_SERVER = "http:\/\/' + pxeIp + ':8080\/zabbix"',
        "/opt/thunder_web/thunder/settings.py"
    )
    