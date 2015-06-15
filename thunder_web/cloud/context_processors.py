# @author: Binoy
# @create_date: 23-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 23-Jan-2015
# @linking to other page: /__init__.py
# @description: Methods for the context processor

#Importing the configurations
from django.conf import settings
from django.db import connection
from cloud.models import *
from thunderadmin.models import *

def baseUrl(request):
    """To clean the site url
    Args:
        {
            self - request from the page          
        }
            
    Returns:
        Returns response to the html page
            
    Raises:
        Exceptions                
    """
    return {'base_url': settings.BASE_URL}

def mediaRoot(request):
    """To find the media root
    Args:
        {
            self - request from the page          
        }
            
    Returns:
        Returns response to the html page
            
    Raises:
        Exceptions                
    """
    return {'media_root': settings.MEDIA_ROOT}

def cloudName(request):
    """To clean the site url
    Args:
        {
            self - request from the page          
        }
            
    Returns:
        Returns response to the html page
            
    Raises:
        Exceptions                
    """
    return {'thunder_name': settings.THUNDER_NAME}

def nodeName(request):
    """To get the name of the node which we have clicked
    Args:
        {
            self - request from the page          
        }
            
    Returns:
        Returns response to the html page
            
    Raises:
        Exceptions                
    """
    
    #to get the total numder of nodes in a cloud
    nodes = Nodelist.objects.filter()
    totalNodes = len(nodes)

    #to get the used node count
    sql = "SELECT * FROM thunder_noderole AS nr INNER JOIN thunder_nodelist AS nl ON nl.id = nr.node_id GROUP BY nr.node_id"
    cursor = connection.cursor()
    cursor.execute(sql);
    node = cursor.fetchall()
    usedNodes = cursor.rowcount
    
    try:
        return {'node_name': request.session['cloudName'], 'node_used': usedNodes, 'node_found': totalNodes, 'cloud_id': request.session['cloudId']}
    except Exception, e:
        
        #passing the values to the template
        return {'node_name': '', 'node_used': usedNodes, 'node_found': totalNodes, 'cloud_id': ''}
    
def getDns(request):
    """To check the dns details are updated
    Args:
        {
            request - request from the page
        }
    Returns:
        Returns response to the html page
            
    Raises:
        Exceptions
    """
    
    #Getting the details about the thunder access.
    thunderAcces = ThunderAcces.objects.all()
    
    #Getting the thunder access details and returning the status
    for thunder in thunderAcces:
        if thunder.dns_ip != '':
            return {'emailSet': False}
        else:
            return {'emailSet': True}

def hasNewAlerts(request):
    """
        Function to check whether any new alerts are availabe.
    """

    # Checks whether any new alerts are there or not
    if Alert.objects.filter(visited = 0).exists():
        return {'hasNewAlerts' : True}
    else:
        return {'hasNewAlerts' : False}
    
def systemSpace(request):
    """To get the system default space
    Args:
        {
            request - request from the page
        }
            
    Returns:
        Returns response to the html page
            
    Raises:
        Exceptions
    """
    return {'system_space': settings.SYSTEM_PARTITON_SPACE}