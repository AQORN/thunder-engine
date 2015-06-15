# @author: Binoy
# @create_date: 16-Apr-2015
# @modified by: binoy    
# @modified_date: 16-Apr-2015
# @linking to other page: 
# @description: manage cron job module

# importing required modules
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thunder.settings")
from cloud.models import *
from cloud.views import *
from network.functions import *
from network.dhcp import *
import re
from django.core.validators import validate_ipv46_address
from deployment.common import *

# Reading the dhcp file
executeCommand("cobbler sync")
sysCredInfo = getSystemCredentials()

# parse lease file to get new nodes
leaseParser = DhcpLeasesParser(settings.DHCP_LEASES_FILE_LOC)
leaseParser.parse()

# Returns the list of active hosts/leases
leaseList = leaseParser.get_hosts()

# loop through the leases list
for leaseInfo in leaseList:    
    
    # creating the node list            
    try:
        ip = leaseInfo['ip_addr']
        nodeList = Nodelist.objects.get_or_create(node_ip = ip)
        nodeInfo = nodeList[0]
    except Exception, e:
        debugException("Ip not valid: " + str(e))
        continue
    
    # Checking if new node created
    if nodeList[1] == True:
        
        # updating the node list with the new host name
        hostName = settings.NODE_PREFIX + str(nodeInfo.id)
        nodeInfo.host_name = hostName
        nodeInfo.user_name = sysCredInfo['username']
        nodeInfo.password = sysCredInfo['password']
        nodeInfo.sudo_password = sysCredInfo['sudo']
        nodeInfo.save()
        
        # Setting the zabbix details
        params = {
            "host": hostName,
            "groups": [{"groupid": settings.ZABBIX_GROUPID}],
            "templates": [{"templateid": settings.ZABBIX_ICMP_TEMP_ID}],
            "interfaces": [{
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": 10050
            }],
        }
        
        # Creating the host in zabbix server
        try:
            zabbixHost = zabbixHostCreate(params)
            nodeInfo.zabbix_host_id = zabbixHost['hostids'][0]
            nodeInfo.save()
            saveJobNodeLog(0, nodeInfo, 'Created host ' + hostName + ' in the zabbix server', 'Created  node in the zabbix server with IP '+ ip +'.', 1)
        except Exception, e:
            errMsg = 'Adding host ' + hostName + ' to zabbix server Failed'
            debugException(errMsg + str(e))
            saveJobNodeLog(0, nodeInfo, errMsg, errMsg, 0)
        
        # parameters for the node alert
        params = {
            'alert_type': 'Node', 
            'referece_id': nodeInfo.id,
            'alert_content': 'New node '+ nodeInfo.host_name +' found', 
            'alert_status' : 'N'
        }
        thunderAlertAdd(params)
        
        # Saving the node details into the node log
        showMsg = 'New node with IP '+ ip +' detected and it added to the thunder'
        saveJobNodeLog(0, nodeInfo, showMsg, showMsg, 1)
        print showMsg

        # checking the mac address, if it available addign it to the node spec
        macId = leaseInfo['mac_addr'] if leaseInfo.has_key('mac_addr') else "" 
        NodeSpec.objects.filter(nodelist_id = nodeInfo.id).delete()
        nodeSpec = NodeSpec(nodelist_id = nodeInfo.id, mac_id = macId).save()
        showMsg = 'Node specification is updated with mac id: '+ macId
        saveJobNodeLog(0, nodeInfo, showMsg, showMsg, 1)
        print showMsg
        
        
'''
###
if node is up, find dynamic details of node like ram, cpu, HDD, nics
and update in DB
###
'''

# select nodes are active with bootstrap image but not updated node details
resList = Nodelist.objects.filter(preos = 0, node_up = 1)

# loop through nodelist
for nodeInfo in resList:
        
    # save nod edynamic details
    callStatus = updateDynamicNodeInformation(nodeInfo)
        
    # save pre os variable if sccessfully saved
    if callStatus:
        nodeInfo.preos = 1
        nodeInfo.save()


'''
###
create static conf to prevent duplicate IP from dhcp server
###
'''

# get all nodes and update dhcpd conf file
resList = Nodelist.objects.all()
staticConf = ""

# loop through node and create string
for nodeInfo in resList:
    
    # get mac id
    try:
        nodeSpec = NodeSpec.objects.get(nodelist_id = nodeInfo.id)
        macId = nodeSpec.mac_id
    except Exception, e:    
        macId = ""
    
    # if mac is not empty
    if macId:
        staticConf += "host " + nodeInfo.host_name + " {\n"
        staticConf += "hardware ethernet " + macId + ";\n"
        staticConf += "fixed-address " + nodeInfo.node_ip + ";\n"
        staticConf += "}\n"

# if content is not empty
if staticConf:
    handle = open(settings.DHCP_STATIC_FILE_LOC, "w")
    handle.write(staticConf)
    handle.close()