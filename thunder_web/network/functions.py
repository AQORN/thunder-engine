# @author: Geo Varghese
# @create_date: 17-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 17-Apr-2015
# @linking to other page: 
# @description: Network related functions

# import required packages
from netaddr import *
from network.models import *
from deployment.environment import *
import os
import random
import collections
from compiler.ast import Node
from django.contrib import messages
from django.utils.safestring import mark_safe
from netaddr import *
from random import randint

def isValidCidr(cidrVal):
    """
    function to check whetehre valid cidr value
    cidrVal - The value of cidr
    @return [True/False] [valid/invalid]
    """
    
    try:
        
        # initialise and check if ip network value
        networkCidr = IPNetwork(cidrVal) 
        if networkCidr:
            return str(networkCidr.cidr)
        
    except Exception, e:
        debugException(e)
    
    return False


def isCidrEqual(cidrVal, checkCidrVal):
    """
    function to check whether both cidr are equal
    cidrVal - The value of cidr
    checkCidrVal - The compare cidr value
    @return [True/False] [equal/not]
    """
    
    try:
        
        # if ip network value
        if IPNetwork(cidrVal) == IPNetwork(checkCidrVal):
            return True
        
    except Exception, e:
        debugException(e)
    
    return False


def isIpInCidr(ipAddr, cidrVal):
    """
    function to check whether ip in cidr network
    ipAddr -     The IP address in range
    cidrVal - The value of cidr
    @return [True/False] [valid/invalid]
    """
    
    try:
        
        # if ip network value
        if IPAddress(ipAddr) in IPNetwork(cidrVal):
            return True
        
    except Exception, e:
        debugException(e)
    
    return False

def isValidIPRange(fromIp, toIp, cidrVal = ""):
    """
    function to check whether valid ip range value
    fromIp -     The first IP address in range
    toIp -       The last ip in range
    cidrVal - The value of cidr. eg: '192.0.2.0/24'
    @return [True/False] [valid/invalid]
    """
    
    try:
        
        # if valid ip range
        if IPRange(fromIp, toIp):
            
            # if cidr value also check
            if cidrVal:
                
                # if both ip in corresponding network
                if isIpInCidr(fromIp, cidrVal) and isIpInCidr(toIp, cidrVal):
                    return True
                
            else:
                return True
        
    except Exception, e:
        debugException(e)
    
    return False

def getCidrFromSubnet(subnet):
    """
    Function to get the cidr from the subnet 
    subnet - subnet address
    @return cidr value
    """
    cidr = sum([bin(int(x)).count('1') for x in subnet.split('.')])
    return cidr

def getStartIp(startPool):
    """
    Function to get the start ip from the start pool 
    startPool - ip address 
    @return start ip of the network
    """
    ip = IPNetwork(startPool)
    return ip.network


def getBroadcast(cidr):
    """
    Function to get the start ip from the start pool 
    startPool - ip address 
    @return start ip of the network
    """
    ip = IPNetwork(cidr)
    return ip.broadcast

def isIpRangeOverlap(fromIp, toIp, compareFromIp, compareToIp):
    '''
    function to chekc ip ranges overlap each other
    fromIp - The first IP address in range
    toIp - The last ip in range
    compareFromIp - The first IP address in compare range
    compareToIp - The last ip in compare range
    @return [True/False] [overlap/not overlap]
    '''
    
    try:
        
        # initialise and check from or to ip in the comapare range
        ipList = getIPAddressListFromRange(compareFromIp, compareToIp)
        if fromIp in ipList or toIp in ipList:
            return True;
        
    except Exception, e:
        debugException(e)
    
    return False


def getIPAddressListFromRange(fromIp, toIp):
    '''
    function to get Ip address list from range
    fromIp -     The first IP address in range
    toIp -       The last ip in range
    @retunr The list of ip addresses  
    '''
    
    ipList = []
    
    # get ip list from range
    try: 
        ipRangeList = list(iter_iprange(fromIp, toIp))
        
        # loop through ip list
        for ipAddr in ipRangeList:
            ipList.append(str(ipAddr))
        
    except Exception, e:
        debugException(e)
        
    return ipList


def getIPAddressListFromCIDR(cidr, removeGateway = True):
    '''
    function to get Ip address list from CIDR value
    cidr -       The cidr value
    @retunr The list of ip addresses  
    '''
    
    ipList = []
    
    # get ip list from cidr
    try: 
        ip = IPNetwork(cidr)
        ipRangeList = list(ip)
        
        # loop through ip list
        for ipAddr in ipRangeList:
            ipList.append(str(ipAddr))
        
        # remove first iP with 0 start
        ipList.pop(0)
            
        # remove gateway ip from the list
        if removeGateway and ipList:
            ipList.pop(0)
            
    except Exception, e:
        debugException(e)
        
    return ipList


def getNodeInstallationDiskInfo(nodeId):
    '''
    function to get node installation disk 
    nodeId  - The id of node
    @return The name of the disk
    '''
    
    list = DiskDrive.objects.filter(nodelist_id = nodeId, system_space__gt = 0)
    
    # loop through the list
    for diskInfo in list:
        return diskInfo
    
    return False


def getNodeNetworkNIC(nodeId, networkType):
    '''
    function to get network nic of a node
    nodeId  - The id of node
    networkType - The type of network[P/A/M/S]
    @return The name of the interface
    '''
    
    # sql for the getting NIC
    sql = """
    select nic.name, nmap.ip_address, nic.id, nic.mac_address from thunder_network_interface nic, thunder_nic_mapping nmap
    where nic.id=nmap.nic_id and nic.nodelist_id=%d and nmap.network_type='%s'
    """ % (nodeId, networkType)
    
    # get the nic name
    try:        
        cursor = connection.cursor()
        cursor.execute(sql)
        nicInfo = cursor.fetchone()
        
        # check the nic name is not empty
        if nicInfo and nicInfo[0]:
            return nicInfo[0], nicInfo[1], nicInfo[2], nicInfo[3] 
        else:
            return False, False, False, False 
        
    except Exception, e:
        debugException(e)
        return False, False, False, False
    

def verifyIPConnection(ipAddress, fromIpAddr, networkInfo, cloudId, networkType, netmask, vlanTag = False):
    '''
    function to verify iplist connection
    ipAddress - The IP address needs to be checked
    fromIpAddr - The node ip addres from ipAddress checked 
    networkInfo - The information about the network
    cloudId - The id of the cloud
    networkType - The type of network[P/F/A/M/S]
    netmask - The netmaks of the network
    vlanTag - The vlan tag of the network
    '''
    
    msgList = collections.OrderedDict()
    statusMsgList = []
    
    # if ipaddress is empty
    if not ipAddress or not fromIpAddr:
        msgList[" -- No valid ip address found in ip network range to test"] = 0
        return "Failed", msgList
    
    # find all nodes assigned in cloud
    nodeList = Nodelist.objects.filter(cloud_id = cloudId)
    
    # if nodes available
    if nodeList:
        
        index = 1
        
        # find environment name
        cloud = Cloud.objects.get(pk = cloudId)
        envName = generateEnvironmentName(cloud.cloud_name)
        overrideList = {'thunder': {}}
        vlanTag = str(vlanTag) if vlanTag else ""
        mainNodeNic = ""
        chefFromNodeError = False
        
        # loop through the node list
        for nodeInfo in nodeList:
            
            # get nic name
            nicType = "P" if networkType == 'F' else networkType
            nicName, deviceIp, netDeviceId, netDeviceMac = getNodeNetworkNIC(nodeInfo.id, nicType)
            overrideList['thunder']['attach_nic'] = nicName
            
            # if nic name is emoty
            if not nicName:
                msgList[" -- Network not configured in nodes"] = 0
                return "Failed", msgList            
            
            # if first os up the IP in it
            if index == 1:
                mainNodeInfo = nodeInfo
                mainNodeNic = nicName
                overrideList['thunder']['from_node'] = 0
                overrideList['thunder']['attach_ip'] = ipAddress
                overrideList['thunder']['from_ip'] = fromIpAddr
                overrideList['thunder']['netmask'] = netmask
                overrideList['thunder']['vlan_tag'] = vlanTag
                overrideList['thunder']['local_repo_ip'] = settings.LOCAL_REPO_IP
                overrideList['thunder']['pkg_download_url'] = settings.PKG_DOWNLOAD_URL
                overrideList['thunder']['chef_server_ip'] = settings.CHEF_SERVER_IP
                chefCommand = getNodeChefDeploymentCommand(nodeInfo, envName, True) + " --run-list 'recipe[thunder-common::setup_network_ip_temp]'"
            else:
                overrideList['thunder']['from_node'] = 1
                chefCommand = getNodeChefDeploymentCommand(nodeInfo, envName, True) + " --run-list 'recipe[thunder-common::check_ping]'"
            
            # update environment with value
            try:
                outputStr = updateCloudEnvironmentFromValue(cloudId, overrideList)
                
                # if error exist in output
                if "ERROR:" in outputStr:
                    msgList["Internal error occured while setup IP"] = 0
                    statusMsgList.append("Failed")
                    break              
                                    
            except Exception, e:
                debugException(e)
                msgList["Internal error occured while setup IP"] = 0
                statusMsgList.append("Failed")
                break            
                            
            # execute the chef command
            try:
                outputStr = executeChefCommand(chefCommand)
                
                # if error occured while deployment
                if "Chef Client finished" not in outputStr:
                    
                    # if first node
                    if index == 1:
                        msgList[" -- Internal error occured while setup IP in network"] = 0
                    else:
                        msgList[" -- Connection between nodes failed in network"] = 0
                    
                    chefFromNodeError = True
                    statusMsgList.append("Failed")
                    break
                
            except Exception, e:
                debugException(e)
                msgList[" -- Internal error occured while setup IP in network"] = 0
                statusMsgList.append("Failed")
                chefFromNodeError = True
                break         
            
            index += 1
            
        # if not main node and error occured, then clear the settings
        if chefFromNodeError:
            try:
                chefCommand = getNodeChefDeploymentCommand(nodeInfo, envName, True)
                chefCommand += " --run-list 'recipe[thunder-common::down_network_ip]'"
                outputStr = executeChefCommand(chefCommand)
            except Exception, e:
                debugException("while clearing temporary set ip in pingnode" + str(e))    
            
        # remove the settngs from main node where ip is set first
        try:
            overrideList['thunder']['attach_nic'] = mainNodeNic
            overrideList['thunder']['from_node'] = 0
            chefCommand = getNodeChefDeploymentCommand(mainNodeInfo, envName, True)
            chefCommand += " --run-list 'recipe[thunder-common::down_network_ip]'"
            outputStr = updateCloudEnvironmentFromValue(cloudId, overrideList)
            outputStr = executeChefCommand(chefCommand)
        except Exception, e:
            debugException("while clearing temporary set ip config" + str(e))
                
    else:
        msgList[" -- No nodes found to verify network settings"] = 0
        return "Failed", msgList
    
    # check any network verification step failed
    if "Failed" in statusMsgList:
        statusMsg = "Failed"
    else:
        statusMsg = "Success"
        
    return statusMsg, msgList

        
def checkPing(ipAddress):
    '''
    function to check ping
    ipAddress -     The ip address to test
    @return  true / false   active / not active 
    '''
    
    response = os.system("ping -c 1 " + str(ipAddress))
    
    # check response
    if response == 0:
        pingStatus = True
    else:
        pingStatus = False

    return pingStatus


def verifyPublicNetwork(cloudId, networkInfo):
    '''
    function to verify public ip network
    cloudId - The id of the cloud
    networkInfo - The information about the network
    '''
    
    # get net list
    netList = PublicNetwork.objects.filter(thunder_network_details_id = networkInfo.id)
    statusMsg = ""
    allMsgList = collections.OrderedDict()
    msgList = collections.OrderedDict()
    netType = "P"
    
    # if net list is not empty
    if netList:
        
        statusMsg = "Success"
        netmask = getNetworkSubnet(networkInfo, netType)
        vlanTag = networkInfo.public_vlan if networkInfo.public_use_vlan else False
            
        # loop through net list an dcheck first ip list and break
        for netIPInfo in netList:
            ipList = getIPAddressListFromRange(netIPInfo.ip_range_from, netIPInfo.ip_range_to)
            ipAddress = str(random.choice(ipList)) if len(ipList) else ""
            fromIpAddr = str(random.choice(ipList)) if len(ipList) else ""
            [retMsg, msgList] = verifyIPConnection(ipAddress, fromIpAddr, networkInfo, cloudId, netType, netmask, vlanTag)
            networkName = netIPInfo.ip_range_from + " - " + netIPInfo.ip_range_to
            
            # check return status of verification
            if retMsg == "Success":
                allMsgList["Successfully tested public network: " + networkName] = 1
            else:
                statusMsg = "Failed"
                allMsgList["Connection to public network - (" + networkName + ")  failed!"] = 0
                
            allMsgList.update(msgList)
             
    return statusMsg, allMsgList


def verifyFloatingIpNetwork(cloudId, networkInfo):
    '''
    function to verify floating ip network
    cloudId - The id of the cloud
    networkInfo - The information about the network
    '''
    
    # get ip list
    netList = FloatingNetwork.objects.filter(thunder_network_details_id = networkInfo.id)
    statusMsg = ""
    allMsgList = collections.OrderedDict()
    msgList = collections.OrderedDict()
    netType = "F"
    
    # if net list is not empty
    if netList:
        
        statusMsg = "Success"
    
        # loop through net list
        for netIPInfo in netList:
            ipList = getIPAddressListFromRange(netIPInfo.ip_range_from, netIPInfo.ip_range_to)
            ipAddress = str(random.choice(ipList)) if len(ipList) else ""
            fromIpAddr = str(random.choice(ipList)) if len(ipList) else ""
            netmask = getNetworkSubnet(netIPInfo.ip_cidr, netType)
            vlanTag = netIPInfo.vlan_tag if netIPInfo.use_vlan else False
            [retMsg, msgList] = verifyIPConnection(ipAddress, fromIpAddr, networkInfo, cloudId, netType, netmask, vlanTag)
            networkName = netIPInfo.ip_range_from + " - " + netIPInfo.ip_range_to
            
            # check return status of verification
            if retMsg == "Success":
                allMsgList["Successfully tested floating IP network: " + networkName] = 1
            else:
                statusMsg = "Failed"
                allMsgList["Connection to floating IP network - (" + networkName + ")  failed!"] = 0
                
            allMsgList.update(msgList)
             
    return statusMsg, allMsgList


def verifyManagementNetwork(cloudId, networkInfo):
    '''
    function to verify management network
    cloudId - The id of the cloud
    networkInfo - The information about the network
    '''
    
    # get ip list
    statusMsg = "Failed"
    allMsgList = collections.OrderedDict()
    msgList = collections.OrderedDict()
    netType = "M"
    
    # check 
    if networkInfo and networkInfo.in_network_cidr:
        netmask = getNetworkSubnet(networkInfo, netType)
        vlanTag = getNetworkVlanTag(networkInfo, netType)
        netCIDR = networkInfo.in_network_cidr
        statusMsg = "Success"
        ipList = getIPAddressListFromCIDR(netCIDR)
        ipAddress = str(random.choice(ipList)) if len(ipList) else ""
        fromIpAddr = str(random.choice(ipList)) if len(ipList) else ""
        [retMsg, msgList] = verifyIPConnection(ipAddress, fromIpAddr, networkInfo, cloudId, netType, netmask, vlanTag)
            
        # check return status of verification
        if retMsg == "Success":
            allMsgList["Successfully tested Managment network"] = 1
        else:
            statusMsg = "Failed"
            allMsgList["Connection to management network failed!"] = 0
            
        allMsgList.update(msgList)
    else:
        statusMsg = "Failed"
        allMsgList["Management network not found!"] = 0
             
    return statusMsg, allMsgList


def verifyStorageNetwork(cloudId, networkInfo):
    '''
    function to verify storage network
    cloudId - The id of the cloud
    networkInfo - The information about the network
    '''
    
    # get ip list
    statusMsg = ""
    allMsgList = collections.OrderedDict()
    msgList = collections.OrderedDict()
    netType = "S"
    
    # check 
    if networkInfo and networkInfo.st_network_cidr:
        netmask = getNetworkSubnet(networkInfo, netType)
        vlanTag = getNetworkVlanTag(networkInfo, netType)
        netCIDR = networkInfo.st_network_cidr
        statusMsg = "Success"
        ipList = getIPAddressListFromCIDR(netCIDR)
        ipAddress = str(random.choice(ipList)) if len(ipList) else ""
        fromIpAddr = str(random.choice(ipList)) if len(ipList) else ""
        [retMsg, msgList] = verifyIPConnection(ipAddress, fromIpAddr, networkInfo, cloudId, netType, netmask, vlanTag)
            
        # check return status of verification
        if retMsg == "Success":
            allMsgList["Successfully tested storage network"] = 1
        else:
            statusMsg = "Failed"
            allMsgList["Connection to storage network failed!"] = 0
            
        allMsgList.update(msgList)
             
    return statusMsg, allMsgList


def updateDynamicNodeInformation(nodeInfo):
    '''
    function to update dynamic node information
    nodeInfo - The information about the node to log in to the system
    @return     True / False     Success/Fail
    '''
    
    # create chef command
    chefCommand = getNodeChefDeploymentCommand(nodeInfo, "", True) + " --run-list 'recipe[thunder-common::get_node_details]'"
                    
    # execute the chef command
    try:
        outputStr = executeChefCommand(chefCommand)
        
        # if error occured while deployment
        if "Chef Client finished" not in outputStr:                
            return False
                
    except Exception, e:
        debugException(e)
        return False
    
    # parse chef results 
    nodeContent = parseChefResult(outputStr)
    nodeSpecList = NodeSpec.objects.get_or_create(nodelist_id = nodeInfo.id)
    nodeSpec = nodeSpecList[0]
    
    # save network details
    networkContent = parseChefSubResult(outputStr, "NIC_RES")
    callStatus = saveNodeNetworkInfo(nodeInfo, networkContent)
    
    # if call failed
    if not callStatus:
        return callStatus
    
    # save network details
    diskContent = parseChefSubResult(outputStr, "DISK_RES")
    callStatus, totalSpace = saveNodeDiskInfo(nodeInfo, diskContent)
    nodeSpec.hdd = totalSpace
    
    # save node spec values
    cpuCount = parseChefSubResult(outputStr, "SYS_CPU")
    nodeSpec.core = int(cpuCount)
    ramSize = parseChefSubResult(outputStr, "SYS_RAM")
    ramSize = float(ramSize) / 1000
    nodeSpec.ram = round(ramSize)
    nodeSpec.save()
    
    return callStatus


def saveNodeDiskInfo(nodeInfo, diskContent):
    '''
    function to save disk details of a node
    nodeInfo - The information about the node to log in to the system
    diskContent - The disk content details
    @return node disk details details
    '''

    totalSpace = 0
    
    # check json can be parsed
    try:
        diskList = json.loads(diskContent)
    except Exception, e:
        debugException(e)
        return False, totalSpace
    
    # if disk list is not empty
    if diskList:
        
        # delete existing disk details of node
        DiskDrive.objects.filter(nodelist_id = nodeInfo.id).delete()
        index = 1
        defDiskFound = False
        
        # loop through the disk list
        for info in diskList:
            
            # if diskname name is default
            if settings.OS_INSTALLATION_DISK + ":" in info:
                defDiskFound = True
                break
    
        # loop through the disk list
        for info in diskList:
            diskInfo = info.split(":")
            
            # diskname not empty
            if len(diskInfo) >= 2:
                diskName = diskInfo[0]
                
                # if default disk existing
                if defDiskFound:
                    systemSpace = settings.SYSTEM_PARTITON_SPACE if diskName == settings.OS_INSTALLATION_DISK else 0
                else:
                    systemSpace = settings.SYSTEM_PARTITON_SPACE if index == 1 else 0
                
                totalDiskSpace = (int(diskInfo[1]) / 1000000000) 
                diskSpace = totalDiskSpace - systemSpace 
                totalSpace += diskSpace
                
                # save disk details
                DiskDrive(
                    nodelist_id = nodeInfo.id, name = diskName, system_space = systemSpace,
                    storage_space = diskSpace, total_space = totalDiskSpace  
                ).save()
                
                index += 1
    
    # if total space is not empty
    if totalSpace:
        return True, totalSpace
    else:
        return False, totalSpace
    

def saveNodeNetworkInfo(nodeInfo, networkContent):
    '''
    function to save network details of a node
    nodeInfo - The information about the node to log in to the system
    networkContent - The network content details
    @return node network details
    '''
    
    # convert to string and find values   
    networkContent = str(networkContent).replace("=>", ":")
    
    # check json can be parsed
    try:
        networkInfo = json.loads(networkContent)
    except Exception, e:
        debugException(e)
        return False        
        
    defaultNic = networkInfo['default_interface'] if networkInfo.has_key('default_interface') else ""
    nicList = []
    
    # check whetheer network infor details present
    if networkInfo and networkInfo.has_key('interfaces'):
    
        # loop through the network info
        for nicName, nicInfo in networkInfo['interfaces'].items():
            
            # if nicname not loopback address
            if nicName not in ['lo'] and "LOOPBACK" not in nicInfo['flags']:
                
                newNICInfo = {"name": str(nicName)}
                macAddress = ""
                
                # loop through nic info details
                for nKey, nVal in nicInfo['addresses'].items():
                                
                    # find mac address
                    if nVal.has_key("family") and not nVal.has_key("prefixlen"):
                        macAddress = str(nKey)
                        
                    # find default nic
                    if nKey == nodeInfo.node_ip:
                        defaultNic = str(nicName)
                    
                newNICInfo['mac_address'] = macAddress
                nicList.append(newNICInfo)
        
        nicCount = len(nicList)
        
        # if atleast one NIC
        if nicCount:
            defaultNic = defaultNic if defaultNic else nicList[0]['name']
            index = 1
            mgtSet = False
            publicSet = False
            stSet = False
        
            # delete all existing nics
            NetworkInterface.objects.filter(nodelist_id = nodeInfo.id).delete()
            
            # loop through nic
            for nicInfo in nicList:
                                    
                # save nic
                nicIp = nodeInfo.node_ip if defaultNic == nicInfo['name'] else ""
                nicObject = NetworkInterface(
                    nodelist_id = nodeInfo.id, name = nicInfo['name'],
                    mac_address = nicInfo['mac_address']
                )
                nicObject.save()
                networkTypeList = []
                
                # get network type list according to the nic count
                if nicCount == 1:
                    networkTypeList = ["A", "M", "S", "P"]
                elif nicCount == 2:
                    networkTypeList = ["A"] if defaultNic == nicInfo['name'] else ["M", "S", "P"]
                elif nicCount == 3:
                    
                    # find the nic networks
                    if defaultNic == nicInfo['name']:
                        networkTypeList = ["A"]
                    elif not mgtSet:
                        networkTypeList = ["M", "S"]
                        mgtSet = True
                    else:
                        networkTypeList = ["P"]
                        
                elif nicCount > 3:
                    
                    # find the nic networks
                    if defaultNic == nicInfo['name']:
                        networkTypeList = ["A"]
                    elif not mgtSet:
                        networkTypeList = ["M"]
                        mgtSet = True
                    elif not publicSet:
                        networkTypeList = ["P"]
                        publicSet = True
                    elif not stSet:
                        networkTypeList = ["S"]
                        stSet = True
                    
                # map the nic by looping through it
                for networkType in networkTypeList:
                    NetworkInterfaceMapping(
                        nic_id = nicObject.id, network_type = networkType, ip_address = nicIp
                    ).save()
                
                index += 1
            
            return True
            
    return False


def checkNetworkSettingsForDeployment(cloudId, request):
    """
    To check network settings values are updated before the deployment
    cloudId - The id of the cloud
    request - The request parameter
    """
    
    returnValue = True
    networkUrl = '<a href=' + settings.BASE_URL + 'clouds/network/' + '>Network update</a>'
    
    # To check the values are updated for the cloud
    try:
        details = NetworkDetails.objects.filter(cloud_id = cloudId)
    except Exception, e:
        debugException(e)
        return False
    
    # checking that the network details are updated
    if len(details) == 0:
        messages.add_message(request, messages.ERROR, mark_safe("Networking section is not updated properly. Please update the same by clicking " + networkUrl))
        returnValue = False
    
    # Iterating through the network details
    for detail in details:
        
        # if network cidr not updated
        if detail.in_network_cidr == "":
             messages.add_message(request, messages.ERROR, mark_safe("Management Network needs to updated. Please update the same by clicking " + networkUrl))
             returnValue = False

        # if storage cidr not updated
        '''
        if detail.st_network_cidr == "":
            messages.add_message(request, messages.ERROR, mark_safe("Storage Network needs to updated. Please update the same by clicking " + networkUrl))
            returnValue = False
        '''   
            
        # check network settings verified 
        if detail.status == 0:
            messages.add_message(request, messages.ERROR, mark_safe("Please verify the network setting. " + networkUrl))
            returnValue = False 

    # Returning the values
    return returnValue


def checkCloudNodeStatusForDeployment(cloudId, request):
    """
    To check network settings values are updated before the deployment
    cloudId - The id of the cloud
    request - The request parameter
    """
    
    # Getting down nodes
    try:
        nodeList = Nodelist.objects.filter(cloud_id = cloudId, node_up = 0)
        nodeCount = len(nodeList) 
        
        # if nodes with down status in deployment
        if nodeCount > 0:
            messages.add_message(request, messages.ERROR, mark_safe("Some nodes are down. Please check status of nodes"))
            return False
        else:
            return True
        
    except Exception, e:
        debugException(e)
        return False


def getNetworkCIDR(networkInfo, networkType):
    '''
    function to get network CIDR
    networkInfo - The network details object of a cloud
    networkType - The  type of the network
    '''

    try:
        
        # get CIDR col to get details
        if networkType == "P":
            tagCol = "public_cidr"
        elif networkType == "M":
            tagCol = "in_network_cidr"
        elif networkType == "S":
            tagCol = "st_network_cidr"
        elif networkType == "F":
            return networkInfo
        else:
            return False
        
        cidrVal = getattr(networkInfo, tagCol)
        return cidrVal
        
    except Exception, e:
        debugException(e)
        return False
    

def getNetworkSubnet(networkInfo, networkType):
    '''
    function to get network CIDR
    networkInfo - The network details object of a cloud
    networkType - The  type of the network / or cidr
    '''

    try:
        netCIDR = getNetworkCIDR(networkInfo, networkType)
        
        # get CIDR getails
        if netCIDR:
            ip = IPNetwork(netCIDR)
            return str(ip.netmask)
        else:
            return False
        
    except Exception, e:
        debugException(e)
        return False


def getNetworkGateway(networkInfo, networkType):
    '''
    function to get network CIDR
    networkInfo - The network details object of a cloud
    networkType - The  type of the network or cidr
    '''

    try:
        netCIDR = getNetworkCIDR(networkInfo, networkType)
        
        # get CIDR to get getails
        if netCIDR:
            ipList = getIPAddressListFromCIDR(netCIDR, False)
            return ipList.pop(0) if len(ipList) > 0 else False
        else:
            return False
        
    except Exception, e:
        debugException(e)
        return False



def isVlanEnabledForCloud(networkInfo):
    '''
    function to check is vlan enabled in cloud
    networkInfo - The network details object of a cloud
    '''
    
    try:
        
        # check whether vlan enabled
        if networkInfo.public_use_vlan or networkInfo.in_use_vlan or networkInfo.st_use_vlan:
            return True
            
        # check whether floating IP list is enabled with vlan tag
        publicVlanTagList = getNetworkVlanTag(networkInfo, "P")
        
        # if have vlan tags enabled
        if len(publicVlanTagList) > 0:
            return True
    
    except Exception, e:
        debugException(e)
    
    return False
    

def getNetworkVlanTag(networkInfo, networkType, checkFloatingIP = True):
    '''
    function to get network vlan tag id
    networkInfo - The network details object of a cloud
    networkType - The  type of the network
    '''
    
    # get vlan tag details
    try:
        
        # get valn cols to get getails
        if networkType == "P":
            enableCol = "public_use_vlan"
            tagCol = "public_vlan"
        elif networkType == "M":
            enableCol = "in_use_vlan"
            tagCol = "in_vlan"
        elif networkType == "S":
            enableCol = "st_use_vlan"
            tagCol = "st_vlan"
        else:
            return False
        
        # if tag is enabled
        if getattr(networkInfo, enableCol):
            vlanTag = getattr(networkInfo, tagCol)
        else:
            vlanTag = False
            
        # if public check for floating IP vlan tags also
        if checkFloatingIP and networkType == "P":
            
            # initialise and check whether public ip network defined
            vlanTagList = {}
            if networkInfo.public_cidr and vlanTag:
                vlanTagList[networkInfo.public_cidr] = vlanTag
             
            # get floating vlan tags
            floatList = FloatingNetwork.objects.filter(thunder_network_details_id = networkInfo.id)
             
            # for each through the floating IP list
            for ipInfo in floatList:
                 
                # if vlan tag defined add it to the list
                if ipInfo.vlan_tag and ipInfo.use_vlan and ipInfo.ip_cidr:
                    vlanTagList[ipInfo.ip_cidr] = ipInfo.vlan_tag
                     
            return vlanTagList
             
        else:
            return vlanTag
        
    except Exception, e:
        debugException(e)
        return False


def isPublicNetworkConfigured(networkId):
    '''
    function to check is public network configured
    networkId - the id of the network
    '''

    # get public network details
    try:
        
        list = FloatingNetwork.objects.filter(thunder_network_details_id = networkId)
        
        # if floating Ip list is active
        if len(list):
            return True
        
        list = PublicNetwork.objects.filter(thunder_network_details_id = networkId)
        
        # if floating Ip list is active
        if len(list):
            return True
        
    except Exception, e:
        debugException(e)

    return False


def verifyAssignUniqueIpForNodeNIC(cloudId):
    '''
    function to assign unique ip for NIC of a node
    nodeId        The node id of the object
    networkInfo     The network details of cloud
    roleCode        The code of the role deployed to node
    @return     The nic list with IP address
    ''' 
    
    # get all nodes of cloud
    nodeIdList = nodesInCloud(cloudId)
    
    # if nodes is empty
    if len(nodeIdList) == 0:
        return False, "Nodes are not assigned for deployment" 
    
    # get network details
    try:
        networkInfo = NetworkDetails.objects.get(cloud_id = cloudId)
        mgtIpList = getIPAddressListFromCIDR(networkInfo.in_network_cidr)
        stIpList = getIPAddressListFromCIDR(networkInfo.st_network_cidr)        
        pubNetList = PublicNetwork.objects.filter(thunder_network_details_id = networkInfo.id)
        pubIpList = []
        
        # if list not empty
        if len(pubNetList):
            
            # loop through public ip list
            for netIPInfo in pubNetList:
                pubIpList += getIPAddressListFromRange(netIPInfo.ip_range_from, netIPInfo.ip_range_to)
        
        # prepare controller id list
        controllerList = getAllControllers(cloudId)
        controllerIdList = []
                
        # loop through controller list
        for controllerInfo in controllerList:
            controllerIdList.append(controllerInfo['id'])
        
        # get vlan tag details
        publicVlanTag = getNetworkVlanTag(networkInfo, "P")
        mgtVlanTag = getNetworkVlanTag(networkInfo, "M")
        stVlanTag = getNetworkVlanTag(networkInfo, "S")
        
        # check is public network configured
        isPublicNetworkConfig = isPublicNetworkConfigured(networkInfo.id)
        
    except Exception, e:
        debugException(e)
        return False, "Cloud network details are not updated"
    
    # loop through nodes
    for nodeId in nodeIdList:
        
        nodeRoleCodeList = getNodeRoleCodeList(nodeId)    
    
        sql = """
        select nic.name,nmap.network_type, nmap.ip_address 
        from thunder_network_interface nic, thunder_nic_mapping nmap
        where nic.id=nmap.nic_id and nic.nodelist_id=%d
        """ % (nodeId)
                
        # get the nic name
        try:
            
            cursor = connection.cursor()
            cursor.execute(sql)
            list = cursor.fetchall()
            nicMapList = {}
            netInfoList = {}
            assignStatus = True
            
            # loop through the list
            for nicName, netType, netIp in list:
                
                # if key not set
                if not nicMapList.has_key(nicName):
                    nicMapList[nicName] = []
            
                nicMapList[nicName].append(netType)
                netInfoList[netType] = {
                    'nic_name': nicName,
                    'net_ip': netIp
                }            
            
            # check all networks are configured in node
            if set(dict(netTypeList).keys()) != set(netInfoList.keys()):
                return False, "All networks are not configured in nodes"            
            
            # loop through net list and check for errors
            for nicName, networkList in nicMapList.iteritems():
                                
                # if one nic have more than 1 network assigned
                if len(networkList) > 1:
                    
                    nicWithOutVlanCount = 0
                    
                    # loop through netwok list
                    for netType in networkList:
                        
                        # if admin network, check Ip is already assigned
                        if netType == "A":
                            
                            # if ip set just continue
                            if netInfoList[netType]['net_ip']:
                                continue
                            else:
                                return False, "Admin network have no IP address assigned"
                            
                        else:
                            
                            # if vlan tag is enabled
                            if getNetworkVlanTag(networkInfo, netType, False):
                                
                                # check network types
                                if netType == "P":
                                    
                                    # if controller node add Ip
                                    if nodeId in controllerIdList:
                                        assignStatus = assignIPToNodeNic(cloudId, nodeId, nicName, netType, pubIpList, netInfoList[netType]['net_ip'])
                                    else:
                                        continue
                                    
                                else:
                                    rangeList = mgtIpList if netType == "M" else stIpList 
                                    assignStatus = assignIPToNodeNic(cloudId, nodeId, nicName, netType, rangeList, netInfoList[netType]['net_ip'])
                            else:
                                
                                # check type of networks, if optional networks not configured just continue
                                if netType == "S" and not networkInfo.st_network_cidr:
                                    continue
                                elif netType == "P" and not isPublicNetworkConfig:
                                    continue
                                else:
                                    
                                     # check network types
                                    if netType == "P":
                                        
                                        # if controller node add Ip
                                        if nodeId in controllerIdList:
                                            assignStatus = assignIPToNodeNic(cloudId, nodeId, nicName, netType, pubIpList, netInfoList[netType]['net_ip'])
                                        else:
                                            continue
                                        
                                    else:
                                        rangeList = mgtIpList if netType == "M" else stIpList 
                                        assignStatus = assignIPToNodeNic(cloudId, nodeId, nicName, netType, rangeList, netInfoList[netType]['net_ip'])
                                    
                                    nicWithOutVlanCount += 1
                    
                    # if more than one network on nic with out vlan tag show error            
                    if nicWithOutVlanCount > 1:
                        return False, "More than one network configured on single network device"
                            
                else:
                    
                    # loop through netwok list
                    for netType in networkList:
                    
                        # if admin network, check Ip is already assigned
                        if netType == "A":
                            
                            # if ip set just continue
                            if netInfoList[netType]['net_ip']:
                                continue
                            else:
                                return False, "Admin network have no IP address assigned"
                                
                        elif netType == "P":
                            
                            # if controller node add Ip
                            if nodeId in controllerIdList:
                                assignStatus = assignIPToNodeNic(cloudId, nodeId, nicName, netType, pubIpList, netInfoList[netType]['net_ip'])
                            else:
                                continue
                        else:
                            rangeList = mgtIpList if netType == "M" else stIpList 
                            assignStatus = assignIPToNodeNic(cloudId, nodeId, nicName, netType, rangeList, netInfoList[netType]['net_ip'])
                        
                # if failed assigning IP
                if not assignStatus:
                    return False, "Network IP assign failed! Please configure network devices properly"
                            
        except Exception, e:
            debugException(e)
            return False, "Network IP assign failed! Please configure node network devices properly"
    
    return True, "Success"


def assignIPToNodeNic(cloudId, nodeId, nicName, netType, ipRangeList, nicIp):
    """
    function to assign unique IP to the nic
    cloudId  - The cloud id
    nodeId - The node id
    nicName - nic name
    netType - The nework type[P,M,S,A]
    ipRangeList - The ip range list
    nicIp - The current Ip of NIC
    """
    
    # check the current IP already in the range
    if nicIp and nicIp in ipRangeList:
        return True
    
    # if no IP available in range
    if len(ipRangeList) == 0:
        return False 

    # get existing ips assigned for a network
    assignedIpList = []
    sql = """
    select nmap.ip_address, nic.id from thunder_network_interface nic, thunder_nic_mapping nmap, thunder_nodelist node
    where nic.id=nmap.nic_id and nic.nodelist_id=node.id and node.cloud_id=%d and nmap.network_type='%s'
    """ % (int(cloudId), netType)

    # assign IP
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        list = cursor.fetchall()
        
        # loop through the list
        for ipAddr, nicId in list:
            
            # check whether IP address is valid
            if ipAddr:
                assignedIpList.append(ipAddr)        
        
        # remove assigned from available list
        availableIpList = [x for x in ipRangeList if x not in assignedIpList]
                
        # if available ip list is not empty
        if len(availableIpList):
            nicIpAddress = random.choice(availableIpList)
            
            # save ip address in the nic
            try:
                networkCardInfo = NetworkInterface.objects.get(
                    nodelist_id = nodeId, name = nicName
                )
                nicMapInfo = NetworkInterfaceMapping.objects.get(
                    nic_id = networkCardInfo.id, network_type = netType
                )
                nicMapInfo.ip_address = nicIpAddress
                nicMapInfo.save()
                return nicIpAddress
            except Exception, e:
                debugException(e)
            
    except Exception, e:
        debugException(e)
    
    return False


def get_net_size(netMask):
    """
        Function to get the netsize for the subnet
    """

    # Initialising the string variable
    binaryStr = ''

    # Calculating the netsize for subnet from netmask
    for octet in netMask:
        binaryStr += bin(int(octet))[2:].zfill(8)

    return str(len(binaryStr.rstrip('0')))

def getSubnetFromNetMaskAndIP(netMask, ip):
    """
        Function to get the subnet value
    """

    # Initilaise the data variable
    returnData = []

    # Splits the string
    netMask = netMask.split('.')
    ip = ip.split('.')

    # calculate network start
    netStart = [str(int(ip[x]) & int(netMask[x]))
        for x in range(0, 4)]

    # Joins the value to make it a string
    subnet = '.'.join(netStart)

    # Sets the return obj
    returnData.append(subnet)
    returnData.append(get_net_size(netMask))

    return returnData

def getRandomIpFromSubnet(subnet):
    """
        Get a random ip addr from the subnet
    """

    # Get the ip list from provided subnet
    ipListObj = IPNetwork(subnet)
    ipList = list(ipListObj)

    # Get a random pointer and return the ip from the list
    randInt = randint(0, len(ipList))
    ipObj = ipList[randInt]

    return str(ipObj)