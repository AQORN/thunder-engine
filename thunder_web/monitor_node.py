# @author: Binoy
# @create_date: 17-Apr-2015
# @modified by: binoy    
# @modified_date: 17-Apr-2015
# @linking to other page: 
# @description: manage cron job module

# importing required modules
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thunder.settings")
from cloud.models import *
from cloud.views import *
import re
from django.db import connections
from deployment.common import *

cursor = connections['zabbix'].cursor()

# Getting all the nodes in the system
nodes = Nodelist.objects.all()

# Looping through the nodes
for node in nodes:
    
    # Creating the sql query to fetch the details from the history table.
    try:
            
        currStatus = isNodeActive(node.host_name)
        preStatus = node.node_up
        
        # check both status are not equal, then add it to alert
        if currStatus != preStatus:
            
            # save current node status
            node.node_up = currStatus
            node.save()
            
            # if node is up
            if currStatus:
                
                # parameters for the zabbix alert
                msgTxt = 'Node '+ node.host_name +' is UP.'
                params = {
                    'alert_type': 'Node', 
                    'referece_id': node.id,
                    'alert_content': msgTxt, 
                    'alert_status' : 'S'
                }
                thunderAlertAdd(params, True)
                
                # Saving the node details into the node log
                saveJobNodeLog(0, node, msgTxt, msgTxt, 1)
                print 'up........'
            
            else:
                
                # parameters for the zabbix alert
                msgTxt = 'Node '+ node.host_name +' is Down.'
                params = {
                    'alert_type': 'Node', 
                    'referece_id': node.id,
                    'alert_content': msgTxt, 
                    'alert_status' : 'F'
                }
                thunderAlertAdd(params, True)
                
                # Saving the node details into the node log
                saveJobNodeLog(0, node, msgTxt, msgTxt, 0)
                print 'Down........'
                
    except Exception, e:
        print e


'''
###
check existing services are down like cobbler,chef, zabbix etc
If down enable it
###
'''        
        
# Getting the services from the tables
getServices = MonitorService.objects.filter(status = 1)

# looping through the services available
for getService in getServices:
    
    # Get the service status
    outputStr = getServiceDetails(getService.command)
    
    # if error occurred while deployment
    if "down" in outputStr:
        executeServiceCommnd(getService.name)
        