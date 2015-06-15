# @author: Geo Varghese
# @create_date: 10-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 10-Mar-2015
# @linking to other page: 
# @description: deployment environment functions

# importing required modules
import json
from cloud.common import *
from deployment.common import *
from deployment.databag import *
from network.functions import *
from network.models import *
from network.functions import *
from django.db import connection
import urlparse
from django.conf import settings

def replaceKnifeFileContent(thunderIP):
    '''
    function to replace knife.rb content
    thunderIP - The IP of the thunder
    '''
    
    # read data
    from cloud.common import *
    fileName = CHEF_REPO_DIR + "/.chef/knife.rb"
    f = open(fileName, 'r')
    fileData = f.read()
    f.close()
    replaceText = 'chef_server_url "https://' + thunderIP + '/organizations/aqorn"'
        
    # if replace text not in file data
    if not replaceText in fileData:
    
        # replace data and write
        newData = re.sub(r'chef_server_url .*', replaceText, fileData)
        f = open(fileName, 'w')
        f.write(newData)
        f.close()


def updateCloudEnvironmentOptions(cloudId, specList):
    '''
    function to update cloud options in the environment array
    cloudId  - The id of teh cloud
    specList  - The  cloud spec list
    @return specList  - The spec list of cloud with updated options
    '''
    
    # get all options available for thunder    
    optColListList = ThunderOption.objects.all()
    overrideValList = {}    
    
    # get all options saved for cloud
    optionValList = ThunderOptionValue.objects.filter(cloud_id = cloudId)
    
    # loop through it to override default value list
    for optVal in optionValList:
        overrideValList[optVal.option_id] = optVal.option_value
            
    # loop through the system available option column list
    for optionVal in optColListList:
        
        specAttrList = []
        assignVal = overrideValList[optionVal.id] if overrideValList.has_key(optionVal.id) else optionVal.default_value
        
        # assign if username col id
        if (optionVal.option_column == 'Default_Username'):
            specAttrList = ['openstack', 'identity', 'admin_user']
            
        elif (optionVal.option_column == 'Default_Tenant'):
            specAttrList = ['openstack', 'identity', 'admin_tenant_name']
            
        elif (optionVal.option_column == 'defaultemail'):
            specAttrList = ['openstack', 'identity', 'admin_email']
            
        elif optionVal.option_column == 'Auto_start_guests_when_host_boots':
            specAttrList = ['openstack', 'compute', 'config', 'start_guests_on_host_boot']
            assignVal = True if (assignVal == 'on') else False
            
        elif optionVal.option_column == 'Use_RAW_images_for_guests_instead_of_QCOW':
            specAttrList = ['openstack', 'compute', 'libvirt', 'images_type']
            assignVal = 'raw' if (assignVal == 'on') else 'default'
            
        elif optionVal.option_column == 'Enable_NOVA_quotas':
            specAttrList = ['thunder', 'enable_nova_quotas']
            assignVal = True if (assignVal == 'on') else False
        
        # if check spec attribute list is not empy
        if specAttrList:
            assignSpecAttribute(specAttrList, specList['override_attributes'], assignVal)
    
    return specList;


def updateNodeNicInEnvironment(cloudId, nodeInfo, specList):
    '''
    function to update node nic configurations in environment
    cloudId  - The id of the cloud
    nodeInfo  - The node object
    specList  - The  cloud spec list
    @return specList  - The spec list of cloud with updated options
    '''
    
    status = False
    
    # get nic details and update in env
    try:
        
        nodeId = nodeInfo.id
        networkInfo = NetworkDetails.objects.get(cloud_id = cloudId)
        from network.functions import *        
        sql = """
        select nic.name,nmap.network_type, nmap.ip_address 
        from thunder_network_interface nic, thunder_nic_mapping nmap
        where nic.id=nmap.nic_id and nic.nodelist_id=%d
        """ % (nodeId)
        cursor = connection.cursor()
        cursor.execute(sql)
        list = cursor.fetchall()        
        networkList = {}
        nodeIp = ""
        publicVlanTag = False
        bridgePortMap = {}
            
        # loop through the list
        for nicName, netType, nicIp in list:
            
            # if storage network not configured
            if netType == "S" and not networkInfo.st_network_cidr:
                continue            
            
            vlanTag = getNetworkVlanTag(networkInfo, netType)
            networkList[netType] = {
                'nic_name': nicName,
                'nic_ip': nicIp,
                'subnet': getNetworkSubnet(networkInfo, netType),
                'gateway': getNetworkGateway(networkInfo, netType),
            }
            
            # if management network set node ip as mangement IP
            if netType == 'M':
                nodeIp = nicIp
                
            # if public network
            if netType == 'P':
                floatNetList = {}
                networkList[netType]['vlan_tag'] = ''
                pubNetBridge = "br-ex"
                pubNetNic = nicName
                pubNetName = "physnet1"
                pubNetDef = "physnet1"
                bridgeNetMap = ""
                networkDef = ""
                
                # loop through the vlan tag list and find floating ip diffrent network
                for cidrVal, tagVal in vlanTag.iteritems():
                    publicVlanTag = True
                    
                    # if main public network cidr and check vlan tag existing for the public network
                    if cidrVal == networkInfo.public_cidr and vlanTag[cidrVal]:
                        networkList[netType]['vlan_tag'] = vlanTag[cidrVal]
                        pubNetVlanStr = str(networkList[netType]['vlan_tag'])
                        pubNetBridge += pubNetVlanStr
                        pubNetNic = nicName + "." + pubNetVlanStr
                        pubNetName = "physnet" + pubNetVlanStr
                        pubNetDef = pubNetName + ":" + pubNetVlanStr + ":" + pubNetVlanStr
                    else:
                        tagVal = str(tagVal)
                        floatNetList[cidrVal] = {
                            'vlan_tag': tagVal,
                            'subnet': getNetworkSubnet(cidrVal, "F"),
                            'gateway': getNetworkGateway(cidrVal, "F"),
                        }
                        brName = "br-ex" + tagVal
                        bridgePortMap[brName] = nicName + "." + tagVal 
                        bridgeNetMap += ",physnet" + tagVal + ":" + brName 
                        networkDef = ",physnet" + tagVal + ":" + tagVal + ":" + tagVal
                
                networkList[netType]['float_net_list'] = floatNetList
                
                # if main public network defined
                if networkInfo.public_cidr:
                    bridgePortMap[pubNetBridge] = pubNetNic
                    bridgeNetMap = pubNetName + ":" + pubNetBridge + bridgeNetMap
                    networkDef = pubNetDef + networkDef
                    specList['override_attributes']['thunder']['pub_net_bridge'] = pubNetBridge
                else:
                    specList['override_attributes']['thunder']['pub_net_bridge'] = ''  
                    bridgeNetMap = bridgeNetMap[1:]
                    networkDef = networkDef[1:]
                
                specAttrList = ['openstack', 'network', 'openvswitch', 'bridge_mappings']
                assignSpecAttribute(specAttrList, specList['override_attributes'], bridgeNetMap)
                specAttrList = ['openstack', 'network', 'ml2', 'network_vlan_ranges']
                assignSpecAttribute(specAttrList, specList['override_attributes'], networkDef)                                                
            else:
                networkList[netType]['vlan_tag'] = vlanTag if vlanTag else '' 
        
        # check whether admin pxe network and managemnet network set
        if networkList.has_key('A') and networkList.has_key('M') and nodeIp:
            specList['override_attributes']['thunder']['bridge_port_map'] = bridgePortMap
            specList['override_attributes']['thunder']['public_use_vlan'] = publicVlanTag
            specList['override_attributes']['thunder']['node_ip'] = nodeIp
            specList['override_attributes']['thunder']['node_hostname'] = nodeInfo.host_name
            specList['override_attributes']['thunder']['vlan_enabled'] = isVlanEnabledForCloud(networkInfo)
            
            # disable the default l3_agent settings for multiple external network
            specAttrList = ['openstack', 'network', 'l3', 'external_network_bridge']
            assignSpecAttribute(specAttrList, specList['override_attributes'], "")
            specAttrList = ['openstack', 'network', 'l3', 'external_network_bridge_interface']
            assignSpecAttribute(specAttrList, specList['override_attributes'], "")
                        
            # check ip configured correctly for both network
            if networkList['A']['nic_ip'] and networkList['M']['nic_ip']:
                specList['override_attributes']['thunder']['node_network'] = networkList
                return True, specList
            
    except Exception, e:
        debugException(e)
    
    return status, specList


def updateNodeDiskInEnvironment(cloudId, nodeInfo, specList):
    '''
    function to update node disk configurations in environment
    cloudId  - The id of the cloud
    nodeInfo  - The node object
    specList  - The  cloud spec list
    @return specList  - The spec list of cloud with updated options
    '''
    
    status = False
    
    # get disk details and update in env
    try:
        nodeId = nodeInfo.id
        list = DiskDrive.objects.filter(nodelist_id = nodeId)
        diskList = []
        
        # if disk list is empty
        if len(list) == 0:
            return False, specList
                    
        # loop through the list
        for diskInfo in list:
            
            # if assigned space gretaer than total space available
            if diskInfo.system_space + diskInfo.storage_space > diskInfo.total_space:
                return False, specList
            
            # if system space is not empty
            if diskInfo.system_space:
                diskList.append({
                    'device': diskInfo.name,
                    'part_start': "1",
                    'part_end': str(int(diskInfo.system_space * 1000)),
                    'part_type': 'primary',
                    'system': 1,
                    'part_name': diskInfo.name + "1"
                })
                
                specList['override_attributes']['thunder']['os_installation_disk'] = diskInfo.name 
                
            # if storage space is not empty
            if diskInfo.storage_space:
                
                # if system storage space defined
                if diskInfo.system_space:
                    partitionType = 'extended'
                    partStart = (diskInfo.system_space * 1000) + 5
                    part_tag = '2'
                else:
                    partitionType = 'primary'
                    partStart = 1
                    part_tag = '1'
                    
                partEnd = partStart + (diskInfo.storage_space * 1000) 
                diskList.append({
                    'device': diskInfo.name,
                    'part_start': str(int(partStart)),
                    'part_end': str(int(partEnd)),
                    'part_type': partitionType,
                    'system': 0,
                    'part_name': diskInfo.name + part_tag
                })
        
        # check ip configured correctly for both network
        specList['override_attributes']['thunder']['node_disk_list'] = diskList
        return True, specList
        
    except Exception, e:
        debugException(e)
    
    return status, specList


def updateDeploymentEnvironment(cloudId, nodeInfo, roleCode = "", overrideList = {}):
    '''
    function to create environment json and update the chef deployment environment
    cloudId   - The id of the cloud
    nodeInfo  - The node object
    roleCode  - The code of the role deployed to node
    overrideList - The list needs to be updated
    '''
    
    # check cloud existing or not
    try:
        cloud = Cloud.objects.get(pk = cloudId)
    except Cloud.DoesNotExist:
        return "Cloud does not exist"

    # get deployment environment name
    envName = generateEnvironmentName(cloud.cloud_name)
    
    # get cloud specifications and override value list
    cloudSpecList = CloudSpecification.objects.all()    
    cloudSpecValList = CloudSpecValue.objects.filter(cloud_id = cloudId)    
    overrideValList = {}
        
    specList = {
        "name": envName,
        "description": cloud.cloud_name,
        "cookbook_versions": {},
        "json_class": "Chef::Environment",
        "chef_type": "environment",
        "default_attributes": {},
        "override_attributes": overrideList
    }
    
    # loop through override value list and assign in spec id key
    for specVal in cloudSpecValList:
        overrideValList[specVal.spec_id] = specVal
    
    # loop through specifications
    for spec in cloudSpecList:
        specCol = spec.spec_column
        
        # check override value exist
        if overrideValList.has_key(spec.id):
            specVal = overrideValList[spec.id].spec_value
        else:
            specVal = spec.default_value
        
        # split spec col and create json dictionary
        specAttrList = specCol.split("::")
        assignSpecAttribute(specAttrList, specList['override_attributes'], specVal)   
    
    # check whether thunder set or not
    if not specList['override_attributes'].has_key('thunder'):
        specList['override_attributes']['thunder'] = {}
        
    specList['override_attributes']['thunder']['ip'] = settings.THUNDER_HOST
    
    # check whether thunderIP set or not
    if not specList['override_attributes']['thunder']['ip']:
        return "ERROR: Thunder IP not set"
    
    # set all thunder related links
    #replaceKnifeFileContent(settings.CHEF_SERVER_IP)
    specList['override_attributes']['thunder']['chef_server_ip'] = settings.CHEF_SERVER_IP
    specList['override_attributes']['thunder']['local_repo_ip'] = settings.LOCAL_REPO_IP
    specList['override_attributes']['thunder']['pkg_download_url'] = settings.PKG_DOWNLOAD_URL

    # find controller IP
    controllerList = getAllControllers(cloudId, "M")
    specList['override_attributes']['thunder']['controller_list'] = []
    
    # assign role code
    specList['override_attributes']['thunder']['role_code'] = roleCode
    
    # if controller ip not found
    if not controllerList or not controllerList[0]['ip']:
        return "ERROR: Controller IP is not set or Controller role not assigned"
    else:
        from network.functions import *
        controllerNic, controllerIP, netDeviceId, netDeviceMac = getNodeNetworkNIC(controllerList[0]['id'], 'M')
        specList['override_attributes']['thunder']['controller_ip'] = controllerIP
    
    # create controller list in env
    for controllerInfo in controllerList:
        specList['override_attributes']['thunder']['controller_list'].append(controllerInfo['ip'])
       
    # update cloud option details
    specList = updateCloudEnvironmentOptions(cloudId, specList)
    
    # update cloud network details
    specList = updateCloudNetworkEnvironment(cloudId, specList)
    
    # update node nic configurations in environment
    updateStatus, specList = updateNodeNicInEnvironment(cloudId, nodeInfo, specList)
     
    # if false then return with error
    if not updateStatus:
        return "ERROR: Network interface configurations are not correct"
     
    # update node disk configurations in environment
    updateStatus, specList = updateNodeDiskInEnvironment(cloudId, nodeInfo, specList)
     
    # if false then return with error
    if not updateStatus:
        return "ERROR: Disk configurations are not correct"
    
    # update the databag names in env
    for listName, listLabel in dataBagCatList:
        specAttrList = ['openstack', 'secret', listName + "_data_bag"]
        assignSpecAttribute(specAttrList, specList['override_attributes'], getDataBagName(listName, cloudId))

    # create json environment file
    from cloud.common import *
    envJsonFile = CHEF_REPO_DIR + "/environment/" + envName + ".json"
    f = open(envJsonFile, 'w')
    f.write(json.dumps(specList))
    f.close()
    
    # update chef environment using the env file
    chefCommand = "knife environment from file " + envJsonFile
    from deployment.common import *
    outputStr = executeChefCommand(chefCommand)
    return outputStr


def updateCloudNetworkEnvironment(cloudId, specList):
    '''
    function to update cloud network in the environment array
    cloudId  - The id of the cloud
    specList  - The  cloud spec list
    @return specList  - The spec list of cloud with updated options
    '''    
        
    try:
        network = NetworkDetails.objects.get(cloud_id = cloudId)
        networkId = network.id 
    except NetworkDetails.DoesNotExist:
        print "No network found for cloud"
        return specList
    
    # get floating ips list
    from network.functions import *
    specList['override_attributes']['thunder']['floatingip_list'] = {}
    floatingIPList = FloatingNetwork.objects.filter(thunder_network_details_id = networkId).order_by('id')
    allFloatIpList = collections.OrderedDict()
    
    # loop through floating Ip list
    for floatingIP in floatingIPList:
        
        cidrVal = isValidCidr(floatingIP.ip_cidr)
        
        # if all floating ip list not having cidr key 
        if not allFloatIpList.has_key(cidrVal):
            allFloatIpList[cidrVal] = []
        
        
        # if valn tag existing
        if floatingIP.use_vlan and floatingIP.vlan_tag:
            vlanTag = str(floatingIP.vlan_tag)
            extNetName = "physnet" + vlanTag
        else:
            vlanTag = ""
            extNetName = "physnet1" 
        
        ipInfo = {
            "ip_range_from": floatingIP.ip_range_from,
            "ip_range_to": floatingIP.ip_range_to,
            "ip_cidr": cidrVal,
            "vlan_tag": vlanTag,
            "ext_net_name": extNetName,
        }
        allFloatIpList[cidrVal].append(ipInfo)
        
    specList['override_attributes']['thunder']['floatingip_list'] = allFloatIpList
    
    # get private cidr list
    specList['override_attributes']['thunder']['private_netlist'] = {}
    privateNetList = PrivateNetwork.objects.filter(thunder_network_details_id = networkId)
    
    # loop through private net list
    for netInfo in privateNetList:
        ipInfo = {
            "ip_cidr": netInfo.network_cidr
        }
        specList['override_attributes']['thunder']['private_netlist'][netInfo.id] = ipInfo
    
    # get dns servers
    dnsList = DNSServer.objects.filter(thunder_network_details_id = networkId)
    
    # if queryset is not empty
    if dnsList.exists():
        
        specAttrList = ['openstack', 'network', 'dhcp', 'upstream_dns_servers']
        assignSpecAttribute(specAttrList, specList['override_attributes'], [])
    
        # loop through dns servers
        for dnsIP in dnsList:
            specList['override_attributes']['openstack']['network']['dhcp']['upstream_dns_servers'].append(dnsIP.dns_server)
    
    # set gre tunnel id range
    tunnelIdRange = str(network.gre_tunnel_from) + ":" + str(network.gre_tunnel_to)
    specAttrList = ['openstack', 'network', 'ml2', 'tunnel_id_ranges']
    assignSpecAttribute(specAttrList, specList['override_attributes'], tunnelIdRange)
    
    # set managment and storage cidr
    specAttrList = ['openstack', 'object-storage', 'network', 'proxy-cidr']
    assignSpecAttribute(specAttrList, specList['override_attributes'], network.in_network_cidr)
    specAttrList = ['openstack', 'object-storage', 'network', 'object-cidr']
    objectCidr = network.st_network_cidr if network.st_network_cidr else network.in_network_cidr
    assignSpecAttribute(specAttrList, specList['override_attributes'], objectCidr)
        
    return specList


def getAllControllers(cloudId, netType = 'A'):
    '''
    function to get controller IP
    cloudId  - The id of the cloud
    @return controllerList - The list of controllers
    ''' 
    
    controllerList = []
    controllerIdList = []
    sql = "select nl.id, nl.node_ip from thunder_nodelist nl, thunder_noderole nr, thunder_roletype role"
    sql += " where nl.id=nr.node_id and nr.role_id=role.id and role.role_code='controller'"
    sql += " and nl.status=1 and cloud_id=" + str(cloudId) + " order by id"
        
    # use cursor to get the controller assigned IP
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        # if row is not none
        for row in rows:
            controllerIPInfo = {}
            controllerIPInfo['id'] = row[0]
            controllerIPInfo['ip'] = row[1]
            controllerList.append(controllerIPInfo)
            controllerIdList.append(controllerIPInfo['id'])
            
        # if not admin type do rest of the checking
        if netType != 'A' and len(controllerIdList):
            controllerList = []
            ctrlerListStr = ', '.join(str(x) for x in controllerIdList)
            sql = """
            select nic.nodelist_id, nmap.ip_address from thunder_network_interface nic, thunder_nic_mapping nmap
            where nic.id=nmap.nic_id and nic.nodelist_id in (""" + ctrlerListStr + """) and nmap.network_type='%s'
            """ % (netType)
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            # if row is not none
            for row in rows:
                controllerIPInfo = {}
                controllerIPInfo['id'] = row[0]
                controllerIPInfo['ip'] = row[1]
                controllerList.append(controllerIPInfo)            
        
    except Exception, e:
        debugException(e)
    
        # if attribute exists    
        if hasattr(e, '__cause__'):
            print e.__cause__
        else:
            print "Internal error occured while finding controller IP"
    
    
    return controllerList
    
    
def assignSpecAttribute(specAttrList, specList, specVal):
    '''
    Recursive function to assign spec attribute and create json array
    specAttrList - The assignment attributes array
    specList - The spec json dictionary
    specVal - The spec value
    '''
    
    # pop first element from the spec attr list
    specCol = specAttrList.pop(0)
    
    # if no elements in sepc attr list - stop recursive call
    if not specAttrList:
        specList[specCol] = specVal
    else:
        
        # if no key set, set key for the attr
        if not specList.has_key(specCol):
            specList[specCol] = {}
        
        # recursive call to nest attr assignment    
        assignSpecAttribute(specAttrList, specList[specCol], specVal)
    
    return specList


def generateEnvironmentName(cloudName):
    '''
    function to generate environment name from cloud name
    cloudName - Name of the cloud
    envName - return environment name from cloud name
    '''
    
    envName = cloudName.lower().replace(" ", "_")
    return envName


def updateCloudEnvironmentFromValue(cloudId, overrideList):
    '''
    function to create environment json and update the chef deployment environment
    cloudId   - The id of the cloud
    overrideList - The list needs to be updated
    '''
    
    # check cloud existing or not
    try:
        cloud = Cloud.objects.get(pk = cloudId)
    except Cloud.DoesNotExist:
        return "Cloud does not exist"

    # get deployment environment name
    envName = generateEnvironmentName(cloud.cloud_name)        
    specList = {
        "name": envName,
        "description": cloud.cloud_name,
        "cookbook_versions": {},
        "json_class": "Chef::Environment",
        "chef_type": "environment",
        "default_attributes": {},
        "override_attributes": overrideList
    }
            
    # create json environment file
    from cloud.common import *
    envJsonFile = CHEF_REPO_DIR + "/environment/" + envName + ".json"
    f = open(envJsonFile, 'w')
    f.write(json.dumps(specList))
    f.close()
    
    # update chef environment using the env file
    chefCommand = "knife environment from file " + envJsonFile
    outputStr = executeChefCommand(chefCommand)
    return outputStr
