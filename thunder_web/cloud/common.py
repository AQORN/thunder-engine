# @author: Geo Varghese
# @create_date: 5-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 5-Mar-2015
# @linking to other page: 
# @description: Common system functions

# importing required modules
import collections
import pprint
import re
import os
import datetime
from django.db.models import Q
from django.conf import settings
from zabbix_api import ZabbixAPI
from cloud.models import *
from deployment.common import *
from datetime import datetime
from django.db import connections
from Crypto.Cipher import AES
import base64

# set chef paths
projectPath = settings.THUNDER_ABS_PATH
CHEF_REPO_DIR = projectPath + "/chef-repo"
CHEF_SECRET_FILE = CHEF_REPO_DIR + "/cookbooks/openstack-common/openstack_data_bag_secret"
MASTER_KEY = settings.SECRET_KEY

def zabbixHostCreate(params):
    """
    To create the host in the zabbix server
    Args:
        {
            params - parameter dictionary
        }
    """
    #Setting the zabbix details
    zapi = ZabbixAPI(server = settings.ZABBIX_SERVER)
    zapi.login(settings.ZABBIX_USERNAME, settings.ZABBIX_PASSWORD)
    returnHost = zapi.host.create(params)
    return returnHost

def zabbixHostDelete(hostIdList):
    """
    To delete the host in the zabbix server
    hostIdList - The zabbix host id
    """
    
    try:
        zapi = ZabbixAPI(server = settings.ZABBIX_SERVER)
        zapi.login(settings.ZABBIX_USERNAME, settings.ZABBIX_PASSWORD)
        result = zapi.host.delete(hostIdList)
        return True
    except Exception, e:
        debugException(e)
    
    return False

def nodesInCloud(cloudId):
    """
    To get the details of nodes in a cloud
    cloudId - The id of the cloud
    """
    
    idList = []
    
    # get nodes in cloud
    try:
        nodeLists = Nodelist.objects.filter(cloud_id = cloudId)
            
        # iterating through the nodes
        for nodeList in nodeLists:
            idList.append(nodeList.id)
    
    except Exception, e:
        debugException(e)
    
    return idList


def getNodeRoleCodeList(nodeId):
    '''
    function to get node roles
    nodeId - The id of the node
    '''
    
    codeList = []
    
    # get assigned role codes
    try:
        from deployment.common import *
        roleCodeList = getCloudRoleList()
        list = NodeRole.objects.filter(node_id = nodeId)
        
        # loop through list
        for listInfo in list:
            codeList.append(roleCodeList[listInfo.role_id].role_code)
        
    except Exception, e:
        debugException(e)
        
    return codeList


def thunderAlertAdd(values, force = False):
    """
        To create the thunder alert
        Args:
            {
                values: List with the details of node or cloud
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.
    """

    #Adding the alerts
    try:
        
        # force to crate alert log
        if force:
            Alert(
                alert_type = values['alert_type'], referece_id = values['referece_id'],
                alert_content = values['alert_content'], alert_status = values['alert_status']
            ).save()            
        else:
            created = Alert.objects.get_or_create(alert_type = values['alert_type'], referece_id = values['referece_id'], alert_content = values['alert_content'], alert_status = values['alert_status'])
            
            #Checking the object already available or not, if available then updating the alert with the current date and time.
            if created[1] == False: 
                Alert.objects.filter(alert_type = values['alert_type'], referece_id = values['referece_id'], alert_content = values['alert_content'], alert_status = values['alert_status']).update(visited = 0, updated_time = datetime.now())
    except Exception, e:
        debugException(e)
        

def isNodeActive(hostname):
    """
    function to check whetehr node Ip is active
    hostname - The ip addres of the node
    @return True/False   Active / Inactive 
    """ 

    # To get the details of status
    try: 
        cursor = connections['zabbix'].cursor()
        sql = """select value from history inner join items on items.itemid = history.itemid
        inner join hosts ON hosts.hostid = items.hostid WHERE hosts.name='%s' AND 
        items.key_='icmppingloss' order by clock desc limit 1""" % (hostname)
        cursor.execute(sql);
        info = cursor.fetchone()
        
        # find the status of node
        if info and info[0] != 100:
            return True
        else:
            return False
        
    except Exception, e:
        debugException(e)
        return False
    
    
def nicsInNode(nodeId):
    """
    To get the nic details in a node
    Args:
        {
            nodeId: NodeId
        }
        
    Returns:
        Returns Details of nics
        
    Raises:
        Exceptions and redirection to the login page.
    """
    try:
        
        #Getting the nic details of a node
        nics = NetworkInterface.objects.filter(nodelist = nodeId)
    except Exception, e:
        debugException(e)
        nics = []

    return nics


def getSystemCredentials(osName = "bootstrap"):
    '''
    function to get node credentials to operate chef
    osName - The name of the os
    @return     The credential of the os
    '''

    #Setting the os password 
    osPassword = getSystemPass()
    
    #Setting the system info
    sysInfo = {
        "username": settings.SYS_OS_USERNAME,
        "password": osPassword,
        'sudo': settings.SYS_OS_SUDO,
    }
    
    return sysInfo

def find_between( value, first, last ):
    """To show the list of clouds
    Args:
        {
             value - the string value
             first - first word to search in the line
             last - last word to search in the line
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
     
    result = re.search('%s(.*)%s' % (first, last), value)
    
    # find value in between using regex
    try:
        result = result.group(1)
    except Exception, e:
        debugException(e)
        result = None     
    return result


def debugException(e, printMsg = True, storeMsg = True):
    """
    function to debug the exception
    e  - exception element
    printMsg - The print msg or not
    storeMsg - Store msg or not
    """
    
    # if print msg enabled
    if printMsg:
        print "\n=====Exception =====\n"
        print str(e)
        print "\n=====Exception =====\n"
 
    
def getMap(nic):
    '''
    function to get the nic id
    networkType = network type
    @return = network id
    ''' 
    mapData = NetworkInterfaceMapping.objects.filter(pk = nic)
    return mapData

def encrypt_val(clear_text):
    """
    To encrypt the word to make the password
        Args:
            {
                values: password word
            }
            
        Returns:
            password value
            
        Raises:
            Exceptions and redirection to the login page.
    """
    enc_secret = AES.new(MASTER_KEY[:32])
    tag_string = (str(clear_text) + (AES.block_size - len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))
    return cipher_text

def decrypt_val(cipher_text):
    """
    To decrypt the word to make the password retrieval
        Args:
            {
                values: password word
            }
            
        Returns:
            password value
            
        Raises:
            Exceptions and redirection to the login page.
    """
    dec_secret = AES.new(MASTER_KEY[:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.rstrip("\0")
    return clear_val

def getSystemPass():
    """
    To decrypt the word to make the password retrieval
        Returns: password value
    """
    #Getting the password from the db
    systemPass = SystemPassword.objects.get(name = 'SYSTEM_OS_PASS')
    
    #Decrypting it and returning it
    osPassword = decrypt_val(systemPass.value)
    return osPassword


def replaceFileLine(searchStr, replaceStr, fileName):
    '''
    function to relace a complete line of file with replace string
    searchStr - search pattern
    replaceStr - replace line
    fileName - the name of the file
    '''
    
    from deployment.common import *
    cmdStr = "perl -pi -e 's/" + searchStr + "/" + replaceStr + "/' " + fileName
    executeCommand(cmdStr)
    