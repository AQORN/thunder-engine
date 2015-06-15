# Create your views here.
# @author: Binoy
# @create_date: 19-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 19-Jan-2015
# @linking to other page: /__init__.py
# @description: Functions of the users

# Including the modules
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from cloud.models import *
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.template import RequestContext
from cloud.forms import * 
from pycurl import USERNAME
from lxml.etree import tostring
from django.template import RequestContext
from requests.api import request
from django.contrib.auth.decorators import login_required
from django.db import connection
from jinja2.ext import Extension
from django.template.base import NodeList
from chardet.test import count
from django.contrib import messages
from django.conf import settings
from django.core import serializers
from django.utils import decorators
from django.utils.translation import ugettext as _
from tabination.views import TabView
from logging import Handler
from django.utils import timezone
import json, datetime, random
from django.core.management.base import NoArgsCommand, CommandError
from datetime import date, timedelta, datetime
import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIClient
from django.core.management.sql import sql_all
from cloud.controllers.rbac_controller import *
from cloud.utils.decorators import checkFeatureAccess
from django.db.models import Q, Max
from zabbixmodels import *
from network.models import *
from network.functions import *
from django.utils.safestring import mark_safe
from cloud.common import *
import re
from django.db import connections
import subprocess
import os
from thunderadmin.common import* 
from operator import itemgetter, attrgetter, methodcaller
from django.contrib.auth import authenticate, login as django_login
from cloud.rbac import getDomainRoles

#setting the base url
APIURL = settings.BASE_URL

@login_required
def main_page(request):
    """To show the main page
    Args:
        {
            request - request from the page          
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
    if request.user.id == None:
        return HttpResponseRedirect('/login')
    
    #logger.log_exception('Description')
    #showing the main page
    return render_to_response('main_page.html', RequestContext(request))

@login_required
def user_page(request, username):
    """To show the main page
    Args:
        {
            request - request from the page    
            username - username of the user      
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
    
    #Getting the user details with the user name
    try:
        user = User.objects.get(username = username)
    except:
        raise Http404('Requested user not found.')
    
    #Getting the bookmarks
    bookmarks = user.bookmark_set.all()
    
    #setting the template
    template = get_template('user_page.html')
    
    #setting the variables for the templates
    variables = RequestContext(request, {
        'username': username,
        'bookmarks': bookmarks
    })
    output = template.render(variables)
    
    #sending the response
    return HttpResponse(output)

@login_required
def logout_page(request):
    """To show the main page
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
    
    # Clearing the auth on logout
    if request.session.has_key('auth'):
        del(request.session['auth'])

    #Loggout from the system
    logout(request)
    
    #sending the page to the login
    return HttpResponseRedirect('/login')

def loginUser(request):
    """
        To handle the login redirection
    """

    # sending the page to the login
    return HttpResponseRedirect('/login')

def login(request):
    """To show the main page
    Args:
        {
            request - request from the page
        }

    Returns:
        Returns response to the html page

    Raises:
        Exceptions and redirection to the login page.
    """

    # Redirects to home page, if the session for auth login is already set
    if request.session.has_key('auth'):
        return HttpResponseRedirect('/')

    # Data variable for error message
    errorMsg = ""

    # if the request is for login
    if request.method == 'POST':

        # Sets the post values to variables
        userName = request.POST['username']
        password = request.POST['password']

        # Handles the django authetication
        user = authenticate(username = userName, password = password)

        # If user is found
        if user is not None:

            # If user is active
            if user.is_active:

                # Calls the django login
                django_login(request, user)

                # Set the user auth in session
                request.session['auth'] = {
                                           "userName" : user.username,
                                           "userId" : user.id
                                           }
                return HttpResponseRedirect('/')
            else:

                # Handles disabled acount
                errorMsg = "Your account is disabled."
        else:

            # Handles the invalid login
            errorMsg = "Invalid login attempt."

    # Sets context data
    context = {"error_msg" : errorMsg}

    # sending the page to the login
    return render(request, 'thunderadmin/login.html', context)

@login_required
def index(request):
    """To set the session values and call function to display the list of clouds
    Args:
        {
            request - request from the page
        }

    Returns:
        Returns response to the html page

    Raises:
        Exceptions and redirection to the login page.
    """
    
    #Redirecting to the admin page if the admin not updated properly
    updated = checkAdminUpdated()
    
    #Redirecting to the admin page if it is not updated correctly 
    if  updated != 0:
        return HttpResponseRedirect('/admin')

    # Redirects to home page, if the session for auth login is already set
    if not request.session.has_key('auth'):
        return HttpResponseRedirect('/login')
    
    # Get the cloud and role for the user
    rbacController = RBACController()
    cloudAccessMapData = rbacController.getUserCloudAccess(request.user.id)
    request.session['cloudAccessMapData'] = cloudAccessMapData['userCloudRoleMap'][0]

    # Resetting the cloud details while entering the home page
    if request.session.has_key('cloudId'):
        del(request.session['cloudId'])
    if request.session.has_key('cloudName'):
        del(request.session['cloudName'])

    # Displays the cloud view
    return cloud(request)

@login_required
def cloud(request):
    """To show the list of clouds
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """

    # Resetting the cloud details while entering the home page
    if request.session.has_key('cloudId'):
        del(request.session['cloudId'])
    if request.session.has_key('cloudName'):
        del(request.session['cloudName'])
    
    # Get the cloud and role for the user
    rbacController = RBACController()
    cloudAccessMapData = rbacController.getUserCloudAccess(request.user.id)
    cloudAccessMap = cloudAccessMapData['userCloudRoleMap'][0]
    userCloudList = cloudAccessMap['cloudList']
    cloudList = ','.join(userCloudList)

    #checking the method and validating it else it showing the registration form
    username = request.user.username
    user = User.objects.get(username = username)
    cloud = []

    # Get cloud list based on the role assigned
    if cloudList:
        cloud = Cloud.objects.extra(where = ["id in (%s)" % (str(cloudList))])

    #setting the template
    template = get_template('cloud/cloudlist.html')

    #setting the variables for the templates
    variables = RequestContext(request, {'username': username, 'clouds': cloud})
    output = template.render(variables)

    #sending the response
    return HttpResponse(output)

@login_required
def cloudAdd(request):
    """To show the list of clouds
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """

    # Checks the access control, if not redirect
    if not checkFeatureAccess(request, 'add_cloud'):
        return HttpResponseRedirect(settings.BASE_URL + "?notAuthenticated=1")
    
    #checking the method and validating it else it showing the cloud add form
    if request.method == 'POST':
        
        #Calling the cloud form
        form = CloudForm(request.POST)
        
        #Checking the validation
        if form.is_valid():
           
            #setting the varaible to create
            cloud_name = form.cleaned_data['cloud_name']
            user_id = request.user.id                        
            post = Cloud.objects.create(cloud_name = cloud_name, user_id = user_id)
            
            ##### TODO - Add default domain for the new cloud #####

            # Set the cloud id, domain name etc
            cloudId = post.id
            domainName = cloud_name + "_domain"

            # Creates domain object
            newDomainObj = CloudDomain()
            newDomainObj = CloudDomain.objects.create(name = domainName)
            newDomainId = newDomainObj.id

            # Creates mapping entries for the clouds associated
            cloudDomainMap = CloudDomainMap.objects.create(cloud = Cloud(cloudId), domain = CloudDomain(newDomainObj.id))

            ##### TODO - Add default domain for the new cloud #####

            #parameters for the alert
            params = {'alert_type': 'Cloud', 
                      'referece_id': post.id,
                      'alert_content': "New cloud '" + cloud_name + "' created", 
                      'alert_status' : 'N'
                      }
            
            #calling the function to add the alert
            thunderAlertAdd(params)
            
            #redirecting to the cloud page
            return HttpResponseRedirect('/cloud')
        else:
            
            #showing the form
            context = { 'form': form }    
            return render(request, 'cloud/add.html', context)
    else:
        form = CloudForm()
        context = { 'form': form }         
        return render(request, 'cloud/add.html', context)

@login_required
def cloudEdit(request, id):
    """To show the list of clouds
    Args:
        {
            request - request from the page
            id - id of the cloud
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
    
    # Checks the access control, if not redirect
    if not checkFeatureAccess(request, 'add_cloud'):
        return HttpResponseRedirect(settings.BASE_URL + "?notAuthenticated=1")
    
    #Getting the cloud details using the id
    cloud = Cloud.objects.get(id = id)    
    request.session['cloudId'] = cloud.id
        
    #to show to the user    
    cloud = CloudForm(request.POST)
    context = { 'cloud': cloud }         
    return render(request, 'cloud/edit.html', context)

@login_required
def recipe(request):
    """To show the list of recipe
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
    
    #checking the method and validating it else it showing the cloud add form
    if request.method == 'POST':
        
        #Calling the cloud form
        form = CloudForm(request.POST)
        
        #Checking the validation
        if form.is_valid():
            
            #setting the varaible to create
            cloud_name = form.cleaned_data['cloud_name']
            user_id = request.user.id                        
            post = Cloud.objects.create(cloud_name = cloud_name, user_id = user_id)
            
            #redrecting to the cloud page
            return HttpResponseRedirect('/recipe')
    else:
        form = RecipeForm()
        context = { 'form': form }         
        return render(request, 'recipe/add.html', context)
    
@login_required    
def feedsRecipe(request, id):
    """To show the list of recipe
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
    
    #importing the serializers
    from django.core import serializers
    
    #Adding the recipe data
    recipe = serializers.serialize("json", Recipe.objects.filter(service_id = id))
    return HttpResponse(recipe)

@login_required
def roleList(request, id):
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

    #Getting the value from the cloud and assigning the value to the session.
    request.session['cloudId'] = id 
    cloudData = Cloud.objects.get(pk = id)
    request.session['cloudName'] = cloudData.cloud_name

    #setting the variable
    query = ''
    form = SearchRoleForm({'query' : query})

    #Adding the where condition
    where_condition = ''
    if request.method == 'POST':

        # Set the search query string from post data
        searchStr = str(request.POST.get('query'))
        where_condition = """ AND (roletype.role_typename LIKE '%%%s%%' or nodelist.host_name LIKE '%%%s%%') """ % (searchStr, searchStr)

    #Adding the group by 
    #groupBy = ' GROUP BY `thunder_nodelist`.`id`' 
    groupBy = ''   

    #sql for the data selection  
    cursor = connection.cursor()
    sql = """SELECT `nodelist`.`id`, `noderole`.`role_id`,
            `roletype`.`role_typename`, `nodelist`.`node_ip`,
            `nodelist`.`host_name`, `nodelist`.`status` AS nodestatus,
            `nodespec`.`core` , `nodespec`.`hdd` , `nodespec`.`ram` ,
            `nodespec`.`mac_id`, `noderole`.`id` AS noderoleId, nodelist.node_up FROM `thunder_noderole` as noderole
            INNER JOIN `thunder_nodelist` as nodelist ON ( `noderole`.`node_id` = `nodelist`.`id` )
            INNER JOIN `thunder_roletype` as roletype ON ( `noderole`.`role_id` = `roletype`.`id` )
            INNER JOIN `thunder_nodespec` as nodespec ON ( `nodespec`.`nodelist_id` = `nodelist`.`id`)
            WHERE `noderole`.`assigned` = 1 AND
            `nodelist`.`cloud_id` = %d %s %s """ % (int(request.session.get('cloudId')), where_condition, groupBy)
    
    cursor.execute(sql);
    nodes = cursor.fetchall()
    fieldName = cursor.description

    #setting the data into the dictionary 
    resultsList = {}

    for node in nodes:
        result = {}
        i = 0
                
        #setting the result list
        while i < len(fieldName):
            result[fieldName[i][0]] = node[i]
            if fieldName[i][0] == 'noderoleId':
                percentage = roleProgress(node[i])
                result['jobProgress'] = percentage
            i = i+1
        
        #Getting the nics in a node
        nics = nicsInNode(node[0])
        
        #Setting the length
        result['nics'] = len(nics)
        
        #adding the result into the dictionary 
        if not resultsList.has_key(int(node[0])):
            resultsList[int(node[0])] = result
        else:
            tempDict = resultsList[int(node[0])]
            tempDict['role_typename'] = tempDict['role_typename'] + ", " + result['role_typename']
            resultsList[int(node[0])] = tempDict

    #returning the response to the html
    return render_to_response('node/nodelist.html', {'nodes':resultsList, 'form': form}, context_instance = RequestContext(request))

@login_required
def roleAssignment(request):
    """To show the list of roles and the server to assign
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """

    # Checks the access control, if not redirect
    if not checkFeatureAccess(request, 'deploy_cloud'):
        return HttpResponseRedirect(settings.BASE_URL + "?notAuthenticated=1")
    
    #setting the message show variable
    message_show = False
    
    #checking the submit button is clicked or not    
    if request.method == 'POST':
         
        #getting the values from the table
        selected_role = request.POST.getlist('do_assign[]')
        selected_server = request.POST.getlist('assignode[]')

        #iterating through the roles        
        for role_id in selected_role:
            
            #iterating through selected servers
            for server_id in selected_server:

                #Getting the node list with server id
                nodelists = Nodelist.objects.get(pk = server_id)

                #To check the assigned id of the node, if it 0 then node is not assigned to any cloud
                if nodelists.cloud_id == '0':
                    nodelists.cloud_id = request.session.get('cloudId')
                    nodelists.save()
                
                #searching in the table to find node is already assigned with a role
                search_node_role = NodeRole.objects.filter(node_id = server_id, role_id = role_id, assigned = True)
                
                #checking that the role already assigned to the node
                if len(search_node_role) == 0: 
                    nodeRole = NodeRole.objects.create(node_id = server_id, role_id = role_id)
                    message_show = True
                    
                else:
                    messages.add_message(request, messages.ERROR, 'Role already assigned.')
        
    #getting the role type list
    role = Roletype.objects.all()
    
    #To show the node list ( need to show the nodes which are assigned to the cloud and free nodes)
    nodes = NodeSpec.objects.filter(Q(nodelist__cloud_id = 0))
    
    #Setting the template values
    nodeSpecList = []
    for node in nodes:
        nodeData = {}
        nodeData['id'] = node.id
        nodeData['core'] = node.core
        nodeData['ram'] = node.ram
        nodeData['hdd'] = node.hdd
        nodeData['mac_id'] = node.mac_id
        nodeData['nodelistId'] = node.nodelist_id
        nodeData['host_name'] = node.nodelist.host_name
        nodeData['node_up'] = node.nodelist.node_up
        nics = nicsInNode(node.nodelist_id)
        nodeData['nics'] = len(nics)
        nodeSpecList.append(nodeData)
        
    #To show the message
    if message_show == True :
        messages.add_message(request, messages.SUCCESS, 'Role assignment successful.')
    
    #returning the the respose to the file
    return render_to_response('node/role_assign.html', {'roles':role, 'nodes':nodeSpecList}, context_instance = RequestContext(request))


@login_required
def nodeConfig(request, nodeId, showNicAssignError = True):
    """
        To show the configuration of nodes
        request - request from the page
        nodeId - node id
        showNicAssignError - flag to check whether the nic assignment related messages need to be displayed or not
    """

    #getting the diskDrives list
    diskDrives = DiskDrive.objects.filter(nodelist_id = nodeId)
    
    #Setting the list to save the initial data
    formList = []
    
    #Saving the disk data
    for diskDrive in diskDrives:
        driveData = {}
        driveData['system_space'] = diskDrive.system_space
        driveData['storage_space'] = diskDrive.storage_space
        driveData['diskId'] = diskDrive.id
        driveData['name'] = diskDrive.name
        driveData['total_space'] = diskDrive.total_space
        formList.append(driveData)

    #getting the node networkInterfaces list
    networkInterfaces = NetworkInterface.objects.filter(nodelist_id = nodeId).order_by('-id')
    
    #iterating through the nodes
    ids = []
    for networkInterface in networkInterfaces:
        ids.append(networkInterface.id)

    #Getting the role objects with conditions. 
    mappingDetails = NetworkInterfaceMapping.objects.filter(nic_id__in = ids)
    
    #Setting the form factory
    DiskDriveFormSet = formset_factory(DiskDriveForm, extra = settings.DISKDRIVE_EXTRA)
    
    #Setting the initial form data
    formset = DiskDriveFormSet(initial= formList)
    
    #To show the message
    messageValue = True
    
    # get valan tag details
    vlanTagList = {}
    try:
        cloudId = request.session.get('cloudId')
        networkInfo = NetworkDetails.objects.get(cloud_id = cloudId)
        vlanTagList['M'] = getNetworkVlanTag(networkInfo, "M")
        vlanTagList['S'] = getNetworkVlanTag(networkInfo, "S")
        publicVlanTagList = getNetworkVlanTag(networkInfo, "P")
        vlanTagList['P'] = "None"
        
        # if have vlan tags enabled
        if publicVlanTagList and publicVlanTagList.has_key(networkInfo.public_cidr):
            vlanTagList['P'] = "Multiple" if len(publicVlanTagList) > 1 else publicVlanTagList[networkInfo.public_cidr]
             
    except Exception, e:
        debugException(e)

    # Checking the form is set and posted.
    # Modified the condition to restrict the section for nic assignment request
    if request.method == "POST" and not request.POST.has_key('targetId'):

        #Setting the post values to the form 
        formset = DiskDriveFormSet(request.POST)
        
        #Checking the form is valid or not
        if(formset.is_valid()):
            
            #Looping through the formset values
            for form in formset:

                #Calculating the spaces
                calcSpace = float(form.cleaned_data['system_space']) +  float(form.cleaned_data['storage_space'])
                
                #If the space is less than calculated space , then showing error
                if(float(form.cleaned_data['total_space']) < calcSpace):
                    messages.add_message(request, messages.ERROR, 'Disk drives details are wrong.')
                    messageValue = False
                else:
                    # if the form values are changed then saving it
                    if form.has_changed():
                        
                        # If save error, then showing error
                        if form.save() != 1:
                            messageValue = False
            
        #To show the message to the users
        if messageValue == False:
            messages.add_message(request, messages.ERROR, 'Disk drives save failed.')
        else:
            messages.add_message(request, messages.SUCCESS, 'Disk drives saved successfully.')
            
            #Returning to the list
            return HttpResponseRedirect(settings.BASE_URL + "roles/" + request.session['cloudId'])
            
        return render_to_response('node/configure.html', {'diskDrives' : diskDrives, 'networkInterfaces' : networkInterfaces, 'mappingDetails' : mappingDetails, 'diskDriveForms' : formset, 'vlanTagList' : vlanTagList, 'netTypeList' : netTypeList}, context_instance = RequestContext(request),)

    #Setting the variable for the network error
    networkError = False
    
    #Looping through the network
    for mappingDetail in mappingDetails:
        
        #Getting the vlan tag
        haveTag = getNetworkVlanTag(networkInfo, mappingDetail.network_type)
        
        #Checking the tag
        if haveTag == False:
            
            #Getting other interfaces from the same nic
            mapDatas = NetworkInterfaceMapping.objects.filter(nic = mappingDetail.nic_id)
            
            #Looping through the network map details
            for mapData in mapDatas:
                
                #Checking the network type with the mapdata network type
                #Checking tag is available
                if mapData.network_type != mappingDetail.network_type:
                    hasTag = getNetworkVlanTag(networkInfo, mapData.network_type)
                    
                    #Checking the storage network cidr
                    if (networkInfo.st_network_cidr == '' and mapData.network_type == 'S'):
                        networkError = False
                    else:
                        if hasTag == False:
                            networkError = True
                         
    #returning the the response to the file
    return render_to_response('node/configure.html', {'diskDrives':diskDrives, 
        'networkInterfaces':networkInterfaces, 'mappingDetails': mappingDetails, 
        'diskDriveForms' : formset, 'vlanTagList': vlanTagList, 'netTypeList': netTypeList, 'showNicAssignError' : showNicAssignError, 'nodeId' : nodeId, 'networkError': networkError},
        context_instance = RequestContext(request),
    )

@login_required
def supportTab(request):
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
     
    #returning the response to the html
    return render_to_response('misc/support.html', {}, context_instance = RequestContext(request))

@login_required
def logTab(request):
    """To show the list of logs that are created
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """    
    
    # Setting the list
    cloud_list = getCloudList(request) 
    node_list = getNodeList(request) 
    role_list = getRoleList(request)
    
    # Get the log details
    cursor = connection.cursor()
    sql = """SELECT log.log_type, log.log_title, log.log_details,log.updated_time FROM thunder_nodelog as log
            INNER JOIN thunder_nodelist as list ON list.id = log.node_listid
            INNER JOIN thunder_noderole as role ON list.id= role.node_id order by updated_time desc"""

    cursor.execute(sql)
    logs = cursor.fetchall()
    fieldName = cursor.description

    # Setting the result set
    resultsList = []

    # Loop through the log data
    for log in logs:
        result = {}
        i = 0

        # Loops the field names
        while i < len(fieldName):
            result[fieldName[i][0]] = log[i]
            i = i + 1

        # adding the result into the dictionary
        resultsList.append(result)

    #returning the response to the html
    return render_to_response('misc/log.html', {'resultsList' : resultsList, 'cloud_lists': cloud_list, 'node_lists': node_list, 'role_lists':role_list}, context_instance = RequestContext(request))

class DBHandler(Handler,object):
    """
    This handler will add logs to a database model defined in settings.py
    If log message (pre-format) is a json string, it will try to apply the array onto the log event object
    """

    model_name = None
    expiry = None

    def __init__(self, model = "", expiry = 0):
        #consturstor
        super(DBHandler,self).__init__()
        self.model_name = model
        self.expiry = int(expiry)

    def emit(self,record):
        """To show the list of logs that are created
        Args:
            {
                request - request from the page
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.                
        """ 
        # big try block here to exit silently if exception occurred
        try:
            # instantiate the model
            try:
                model = self.get_model(self.model_name)
            except:
                from logger.models import GeneralLog as model

            log_entry = model(level = record.levelname, message = self.format(record))

            # test if msg is json and apply to log record object
            try:
                data = json.loads(record.msg)
                for key,value in data.items():
                    if hasattr(log_entry,key):
                        try:
                            setattr(log_entry,key,value)
                        except:
                            pass
            except:
                pass

            log_entry.save()

            # in 20% of time, check and delete expired logs
            if self.expiry and random.randint(1,5) == 1:
                model.objects.filter(time__lt = timezone.now() - datetime.timedelta(seconds = self.expiry)).delete()
        except:
            pass

    def get_model(self, name):
        """To getting the model 
        Args:
            {
                self- request from the page
                name - name of the request
            }
            
        Returns:
            Returns response 
            
        Raises:
            Exceptions and redirection to the login page.                
        """ 
        names = name.split('.')
        mod = __import__('.'.join(names[:-1]), fromlist = names[-1:])
        return getattr(mod, names[-1])
   
@login_required
def getCloudList(request):
    """To getting the cloud list
        Args:
            {
                request - name of the request
            }
            
        Returns:
            Returns response 
            
        Raises:
            Exceptions and redirection to the login page.                
    """ 
    
    #getting the cloud list
    cloud_list = Cloud.objects.all()
    return cloud_list

@login_required
def getNodeList(request):
    """To getting the node list
        Args:
            {
                request - name of the request
            }
            
        Returns:
            Returns response 
            
        Raises:
            Exceptions and redirection to the login page.                
    """
    
    #getting the node list 
    node_list = Nodelist.objects.all()
    return node_list

@login_required
def getRoleList(request):
    """To getting the role list
        Args:
            {
                request - name of the request
            }
            
        Returns:
            Returns response 
            
        Raises:
            Exceptions and redirection to the login page.                
    """ 
    
    #getting the role list
    role_list = Roletype.objects.all()
    return role_list   

@login_required
def searchLogs(request):
    """searchLogs
        List all objects with the search criteria
    Args:
        request: HTTP request object passed to the view method by default
    Returns:
        response: HttpResponse
    Raises:
    """
    try:
        
        #adding the where condition
        whereRole = ''
        whereCloud = ''
        whereList = ''
        
        #adding where if it available
        if request.GET['rolelist'] != '':
            whereRole = ' AND role.role_id = ' + request.GET['rolelist']
        
        #adding where if it available    
        if request.GET['cloudlist'] != '':
            whereCloud = ' AND list.cloud_id = ' + request.GET['cloudlist']
            
        #adding where if it available
        if request.GET['nodelist'] != '':
            whereList = ' AND list.id = ' + request.GET['nodelist']     
        
        #making the sql for the search
        cursor = connection.cursor()
        sql = "SELECT log.log_type, log.log_title, log.log_details FROM thunder_nodelog as log  INNER JOIN thunder_nodelist as list ON list.id = log.node_listid  INNER JOIN thunder_noderole as role ON list.id= role.node_id WHERE log.status = 1 " + whereRole + whereCloud + whereList
        cursor.execute(sql)
        logs  = cursor.fetchall()
        fieldName = cursor.description
       
        #setting the result set               
        resultsList = []   
        for log in logs:
            result = {}
            i = 0
            while i < len(fieldName):
                result[fieldName[i][0]] = log[i]
                i = i+1    
            
            #adding the result into the dictionary 
            resultsList.append(result)
                 
        #sending the response
        return HttpResponse(json.dumps(resultsList), content_type = "application/json")

    except Exception, e:
        #Sending the error code
        return HttpResponse("201")  
    
# @author: Binoy
# @create_date: 25-Feb-2015
# @modified by: Binoy M V    
# @modified_date: 25-Feb-2015
# @description: Class for the log delete
class Command(NoArgsCommand):
    args = 'None.'
    help = 'Performs cleaning operations.'
    
    def handle_noargs(self, *args, **options):
        """searchLogs
        List all objects with the search criteria
        Args:
            request: HTTP request object passed to the view method by default
            self: self.
            *args : arguments
            **options: more options
        Returns:
            response: HttpResponse
        Raises:
        """
        
        # delete SystemErrorLog records older than 31 days
        cutoff = datetime.now() - timedelta(days=31)
        records = Log.objects.filter(timestamp__lt = cutoff)
        
        #deleting the recordds
        records.delete()
        return
    
def manageAddons(request):
    """To show the list of Addons and to manage the same.
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
    
    #getting the values from table
    addons = ManageAddons.objects.all()
    
    #returning it to the template
    return render_to_response('misc/addons.html', {'addons':addons}, context_instance = RequestContext(request))  

def removeRole(request):
    """
        To show the list of Addons and to manage the same.
        request - request from the page
    """
    
    #initialing the error stat
    errorStat = False
    
    # Checks the access control, if not redirect
    if not checkFeatureAccess(request, 'deploy_cloud'):
        return HttpResponseRedirect(settings.BASE_URL + "?notAuthenticated=1")
    
    # Checks if posted value is null
    if len(eval(request.POST.get('datepost'))) == 0:
        messages.add_message(request, messages.ERROR, 'Select a role to remove.')
        return HttpResponse('error')

    #getting the ids and looping through it
    for  ids in eval(request.POST.get('datepost')):
        
        #getting the values from the list
        idList = ids.split("-")
         
        #to delete the roles from the noderole table
        nodeRoles = NodeRole.objects.filter(node_id = idList[1])

        #for the role delete
        for nodeRole in nodeRoles:

            #delete job from the job table (actually create another job with job_type as ROLE_REVOKE)
            job = Job.objects.filter(subject_id = nodeRole.id, job_type = 'ROLE_ASSIGN', cloud_id = request.session['cloudId'])

            #deleting the roles if the job is null
            if len(job) > 0:
                
                #To show the error to the user
                messages.add_message(request, messages.ERROR, 'Role assignment cannot be removed.')
                errorStat = True
            else:

                #Deleting the node role and updating the node list with cloud 0
                NodeRole.objects.filter(role_id = nodeRole.role_id, node_id = idList[1]).delete()
                Nodelist.objects.filter(id = idList[1]).update(cloud_id = 0)
    
    #Showing success message to the user.
    if errorStat == False:
        messages.add_message(request, messages.SUCCESS, 'Roles removed successfully.')
        
    return HttpResponse('success')

# def optionsDetails(request):
#     """
#     To show the list of options and to manage the same.
#     Args:
#         {
#             request - request from the page
#         }
#         
#     Returns:
#         Returns response to the html page
#         
#     Raises:
#         Exceptions and redirection to the login page.     
#     """
#     #getting the values from table
#     addons = ManageAddons.objects.all()
#     
#     #returning it to the template
#     return render_to_response('options/options.html', {'addons':addons}, context_instance = RequestContext(request))


def taskDetails(request):
    """
    To show the list of options and to manage the same.
    request - request from the page     
    """
    
    # To check the network values are updated.
    statusList = []
    cloudId = request.session['cloudId']
    statusVal = checkNetworkSettingsForDeployment(cloudId, request)
    statusList.append(statusVal)
    
    # To check the node status
    statusVal = checkCloudNodeStatusForDeployment(cloudId, request)
    statusList.append(statusVal)
    
    # check the number of controllers
    controllerIPList = getAllControllers(cloudId)
    
    # if controller ip list is not empty
    if len(controllerIPList) == 0:
        statusList.append(False)
        messages.add_message(request, messages.ERROR, 'No controller node found for cloud.')
    
    # check whether loud deployment complete or not
    deploymentComplete = isCloudDeploymentComplete(cloudId)
    statusList.append(deploymentComplete)
    
    # If the deployment completed. Delete all jobs
    if deploymentComplete == True:
        Job.objects.filter(cloud_id = cloudId).delete()
    else:
        messages.add_message(request, messages.ERROR, 'Cloud deployment is in progress.')
    
    # enable deploy button or not    
    enableDeploy = False if False in statusList else True

    # If simulator mode, disable cloud deploy
    if settings.SIMULATOR_MODE:
        enableDeploy = False
        
    # returning it to the template
    return render_to_response('task/task.html',
        {'enableDeploy' : enableDeploy},
        context_instance = RequestContext(request)
    )

    
def deployThunder(request):
    """
    To start the deployment on the cloud
    request  - The input details to deploy cloud    
    """
        
    responseData = {}

    # Checks the access control, if not redirect
    if not checkFeatureAccess(request, 'deploy_cloud'):
        return HttpResponseRedirect(settings.BASE_URL + "?notAuthenticated=1")
    
    cloudId = request.session['cloudId']
        
    # check if deployment already in progress
    if not isCloudDeploymentComplete(cloudId):
        responseData['status'] = False
        responseData['text'] = 'Cloud deployment already started!'
        return HttpResponse(json.dumps(responseData), content_type = "application/json")
    
    # verify the node ip assigment 
    status, message = verifyAssignUniqueIpForNodeNIC(cloudId)
    
    # if ip assignment failed
    if not status:
        responseData['status'] = False
        responseData['text'] = message
        return HttpResponse(json.dumps(responseData), content_type = "application/json")
        
    # get assigned roles and add it to jobs
    try:
         
        # get rol code and node list
        roleCodeList = getCloudRoleList()
        nodeIds = Nodelist.objects.filter(cloud_id = cloudId)
        ids = []
        
        # loop through it and get ids
        for nodeId in nodeIds:
            ids.append(nodeId.id)
      
        # Getting the role objects with conditions. 
        nodeRoles = NodeRole.objects.filter(node_id__in = ids).filter(assigned = 1)
          
        # Creating the dictionary and saving the status and text     
        if len(nodeRoles):
             
            #Iterating each roles from the list
            for nodeRole in nodeRoles:
                  
                # setting the job priority
                if roleCodeList.has_key(nodeRole.role_id) and roleCodeList[nodeRole.role_id].role_code == "controller":
                    jobPriority = 1
                else:
                    jobPriority = 2
                  
                # Getting the job or creating the job 
                newJob = Job.objects.get_or_create(
                    cloud_id = cloudId, subject_id = nodeRole.id,
                    job_type = 'ROLE_ASSIGN', job_status = 'N', job_priority = jobPriority
                )
          
                # Adding the node log
                Nodelog.objects.create(
                    node_listid = nodeRole.node_id, subject_id = nodeRole.id, log_type = 'ROLE_ASSIGN', log_title= 'New Role ' +  nodeRole.role.role_typename + ' Assigned.',
                    log_details = 'New Role ' +  nodeRole.role.role_typename + ' is assigned to the node with host name ' + nodeRole.node.host_name 
                )
                 
            responseData['status'] = True
            responseData['text'] = 'Cloud deployment started successfully'            
        else:
            responseData['status'] = False
            responseData['text'] = 'No roles found!' 
        
    except Exception, e:
        print e
        responseData['status'] = False
        responseData['text'] = 'Cloud deployment failed'
            
    #sending the response
    return HttpResponse(json.dumps(responseData), content_type = "application/json")


def insight(request):
    """
    To show the list of options and to manage the same.
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.     
    """
    #getting the values from table
    addons = ManageAddons.objects.all()
    
    #returning it to the template
    return render_to_response('misc/insight.html', {'addons':addons}, context_instance = RequestContext(request))

def configCloud(request):
    """
    To save options and to manage the same.
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.     
    """
    
    message_value = 0
    
    #Checking the post 
    if request.method == 'POST':
        
        #To check the cloud configuration form
        forms = cloudConfigForm(request.POST)
        
        #checkign that the form is valid or not
        if forms.is_valid():
            
            # Checks the access control, if not redirect
            if not checkFeatureAccess(request, 'edit_config'):
                return HttpResponseRedirect(settings.BASE_URL + "?notAuthenticated=1")
            
            #Deleting all the values of CloudSpecValue. This is to update the CloudSpecValue
            CloudSpecValue.objects.filter(cloud_id = request.session['cloudId']).delete()
            
            #Getting the values from the post
            for key in request.POST:
                try:
                    
                    #Getting the values
                    cloud_specs = CloudSpecification.objects.get(spec_column = key)
                    try:
                        cloud_spec_value = CloudSpecValue.objects.get(cloud_id = request.session['cloudId'],  spec_id = cloud_specs.id)
                        
                        #updating to the database
                        if request.POST[key] != '':
                            cloud_spec_value.spec_value = request.POST[key]
                            cloud_spec_value.save()
                            message_value = 1
                            
                    except ObjectDoesNotExist:
                         #inserting to the database
                        if request.POST[key] != '':
                            CloudSpecValue.objects.create(cloud_id = request.session['cloudId'], spec_id = cloud_specs.id, spec_value = request.POST[key])
                            message_value = 2
                    
                except CloudSpecification.DoesNotExist:
                    if key != 'csrfmiddlewaretoken':
                        messages.add_message(request, messages.ERROR, 'Cloud Specification error.'+key) 
    
    else:
        #to show th form with values
        cloudDetails = CloudSpecValue.objects.filter(cloud_id = request.session['cloudId'])    
        initialValue = {}
        
        #Iterating through the values to show into the form
        for cloudItem in cloudDetails:
            initialValue[cloudItem.spec.spec_column] = cloudItem.spec_value
         
        #setting the form values        
        forms = cloudConfigForm(initial = initialValue) 
    
    #to show the message to the user
    if message_value == 1:
        messages.add_message(request, messages.SUCCESS, 'Cloud Specification updated.')
    elif message_value == 2:
        messages.add_message(request, messages.SUCCESS, 'Cloud Specification created.')
    
    #Creating the category dictionary
    categoryDic = dict(map(reversed, SERVICE_LIST))
    categoryDic = dict (zip(categoryDic.values(),categoryDic.keys()))
        
    return render_to_response('cloud/configure.html', {'forms': forms, 'categoryLists': categoryDic}, context_instance = RequestContext(request))

def dataBagConfig(request):
    """
    To save the databag and to manage the same.
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.     
    """
    message_value = 0
     
    #Checking the post 
    if request.method == 'POST':
        
        forms = dataBagConfigForm(request.POST)
        if forms.is_valid():
    
            # Checks the access control, if not redirect
            if not checkFeatureAccess(request, 'edit_config'):
                return HttpResponseRedirect(settings.BASE_URL + "?notAuthenticated=1")
            
            #Deleting all the values of databa. This is to update the databag
            DataBag.objects.filter(cloud_id = request.session['cloudId']).delete()
           
            #iteration through the post values
            for key in request.POST:
                try:
                    
                    #Getting the values
                    databag = DataBagItem.objects.get(item_column = key)
                    
                    try:
                        
                        #Getting the values with item id
                        databag_value = DataBag.objects.get(cloud_id = request.session['cloudId'], item_id = databag.id)
                        
                        #updating to the database
                        if request.POST[key] != '':
                            databag_value.databag_value = request.POST[key]
                            
                            databag_value.save()
                            message_value = 1
           
                    except ObjectDoesNotExist:
                        
                        #inserting to the database
                        if request.POST[key] != '':
                            DataBag.objects.create(cloud_id = request.session['cloudId'], item_id = databag.id, databag_value = request.POST[key])
                            message_value = 2
                        
                except DataBagItem.DoesNotExist:
                    if key != 'csrfmiddlewaretoken':
                        messages.add_message(request, messages.ERROR, 'Databag error.'+key) 
    else:
        #to show th form with values
        databagDetails = DataBag.objects.filter(cloud_id = request.session['cloudId'])    
        initialValue = {}
        
        #Iterating through the values to show into the form
        for bagItem in databagDetails:
            initialValue[bagItem.item.item_column] = bagItem.databag_value
         
        #setting the form values        
        forms = dataBagConfigForm(initial = initialValue) 

    #to show the message to the user
    if message_value == 1:
        messages.add_message(request, messages.SUCCESS, 'Databag updated.')
    elif message_value == 2:
        messages.add_message(request, messages.SUCCESS, 'Databag created.')
        
    #Creating the category dictionary
    categoryDic = dict(map(reversed, dataBagCatList))
    categoryDic = dict (zip(categoryDic.values(),categoryDic.keys()))
    
    return render_to_response('cloud/databag_config.html', {'forms': forms, 'categoryLists': categoryDic}, context_instance = RequestContext(request))

def deleteCloud(request):
    """
    To delete the node role, jobs etc
    request - request from the page     
    """ 

    # Checks the access control, if not redirect
    if not checkFeatureAccess(request, 'del_cloud'):
        return HttpResponseRedirect(settings.BASE_URL + "?notAuthenticated=1")
    
    try:
        cloudId = request.session['cloudId']
        cloudName = request.session['cloudName']
        jobList = Job.objects.filter(cloud_id = cloudId)
        domainList = []
        
        # if job count is empty, just delete the cloud and all node assignment, free node from cloud
        if len(jobList) == 0:

            # To delete the domains / users associated with the cloud
            domainFilterList = CloudDomainMap.objects.filter(cloud = Cloud(cloudId)).distinct()

            # Create the domain list
            for domain in domainFilterList:
                domainList.append(int(domain.domain_id))

            nodeIdList = nodesInCloud(cloudId)
            NodeRole.objects.filter(node_id__in = nodeIdList).delete()
            Nodelist.objects.filter(id__in = nodeIdList).update(cloud_id = 0)
            Cloud.objects.filter(id = cloudId).delete()

            # Delete cloud domains of the cloud
            CloudDomain.objects.filter(id__in = domainList).delete()

            # To delete the users that are not associated with any roles / domain
            cursor = connection.cursor()
            userIds = []

            # sql for the data selection
            sql = "select user.id from auth_user user,thunder_user_role_mapping user_map where user_map.user_id != user.id;"
            cursor.execute(sql)
            userIdList = cursor.fetchall()

            # Create user list
            for id in userIdList:
                
                #Checking the the user id is not equal to logged in user. This is to prevent deletion of logged in user.
                if int(id[0]) != request.user.id:
                    userIds.append(int(id[0]))

            # Deletes the users related to the roles / domain
            User.objects.filter(id__in = userIds).delete()

            params = {
                'alert_type': 'Cloud', 
                'referece_id': cloudId,
                'alert_content': "Cloud '" + cloudName + "' deleted successfully",
                'alert_status' : 'S'
            }
            thunderAlertAdd(params, True)
            messages.add_message(request, messages.SUCCESS, "Cloud '" + cloudName + "' deleted successfully")
            
            #Deleting the session and redirecting it
            delSession(request)
            return HttpResponseRedirect(settings.BASE_URL)
        
    except Exception, e:
        debugException(e)
        messages.add_message(request, messages.ERROR, 'Internal error occured while deleting cloud')
        return HttpResponseRedirect('/')    
    
    # check pending jobs 
    jobList = Job.objects.filter(cloud_id = cloudId, job_status = 'P')
    
    # if pending jobs are there show error message
    if len(jobList) > 0:
        messages.add_message(request, messages.ERROR, "Cloud can't be deleted now, deployment jobs are in pending state")
        return HttpResponseRedirect('/clouds/task')
    
    # get all completed jobs
    jobList = Job.objects.filter(cloud_id = cloudId, job_type = 'ROLE_ASSIGN')
    
    # loop through job list and create revoke jobs
    for jobInfo in jobList:
        roleId = jobInfo.subject_id
        
        # if new job, just delete job and all assignments
        if jobInfo.job_status == 'N':
            NodeRole.objects.filter(pk = roleId).delete()
            jobInfo.delete()
        else:
            jobStatus = Job.objects.get_or_create(
                cloud_id = cloudId, job_type = 'ROLE_REVOKE',
                subject_id = roleId, job_status= 'N'
            )
            
    messages.add_message(request, messages.SUCCESS, "Delete cloud '" + cloudName + "' started")
    return HttpResponseRedirect('/')


@login_required
def getLimitAlert(request):
    """
    To show the list of roles and the server to assign
    request - request from the page                
    """

    #Getting the data from the job and nodelog table
    cursor = connection.cursor()
        
    # Get the cloud and role for the user
    rbacController = RBACController()
    cloudAccessMapData = rbacController.getUserCloudAccess(request.user.id)
    cloudAccessMap = cloudAccessMapData['userCloudRoleMap'][0]
    request.session['cloudAccessMapData'] = cloudAccessMapData['userCloudRoleMap'][0]
    cloudList = ','.join(cloudAccessMap['cloudList'])

    #Checking the request is ajax or not, if ajax then limiting the result, else getting all       
    if request.is_ajax():
        
        #Setting the sql
        sql = "SELECT log.*, job.job_status FROM thunder_nodelog as log INNER JOIN thunder_job AS job ON job.id = log.subject_id INNER JOIN thunder_nodelist AS list ON list.id = log.node_listid  WHERE log.log_type= 'JOB' AND list.cloud_id  IN (" + str(cloudList) + ") ORDER BY log.updated_time desc LIMIT 5"
        cursor.execute(sql);
        logs  = cursor.fetchall()
        fieldName = cursor.description
       
        #setting the data into the dictionary 
        resultsList = []   
        for log in logs:
            result = {}
            i = 0
            while i < len(fieldName):
                result[fieldName[i][0]] = log[i]
                i = i+1    
            
            #adding the result into the dictionary 
            resultsList.append(result)
        
        #returning the the respose to the file
        return render_to_response('misc/alert.html', {'alerts':resultsList}, context_instance = RequestContext(request))
    else:

        # Resetting the cloud details while entering the home page
        if request.session.has_key('cloudId'):
            del(request.session['cloudId'])
        if request.session.has_key('cloudName'):
            del(request.session['cloudName'])

        #getting the selected values from the list 
        alertIds = request.POST.getlist('alertall[]')
        
        #to delete the alert from the log table
        for alertId in alertIds:
            Nodelog.objects.filter(pk = alertId).delete()
            
             
        resultsList = []   
   
        # if cloud list is not empty
        if cloudList:
           
            # getting the jobs from the table
            sql = """SELECT log.*, job.updated_time job_time ,job.job_progress, job.job_status, job.id as jobid FROM thunder_nodelog as log
            INNER JOIN thunder_job AS job ON job.id = log.subject_id
            INNER JOIN thunder_nodelist AS list ON list.id = log.node_listid
            WHERE log.log_type= 'JOB' AND list.cloud_id IN (""" + str(cloudList)  + """)
            ORDER BY job.updated_time desc"""
            cursor.execute(sql)
            logs  = cursor.fetchall()
            fieldName = cursor.description
           
            #setting the data into the dictionary
            for log in logs:
                result = {}
                i = 0
                while i < len(fieldName):
                    result[fieldName[i][0]] = log[i]
                    i = i+1    
                 
                #adding the result into the dictionary 
                resultsList.append(result)
       
        #returning the the respose to the file
        return render_to_response('misc/alert_all.html', {'alerts':resultsList}, context_instance = RequestContext(request))


@login_required
def jobView(request):
    """To show the list of roles and the server to assign
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    #Checking the request is ajax or not, if ajax then limiting the result, else getting all
    if request.is_ajax():
        
        sql = """SELECT * FROM thunder_nodelog as log INNER JOIN
        thunder_job AS job ON job.id = log.subject_id WHERE log.log_type= 'JOB'
        AND log.id = """ + request.POST.get('datapost') + """  ORDER BY job.updated_time"""

        #Getting the data from the job and nodelog table
        cursor = connection.cursor()
    
        #executing the query and fetching the result
        cursor.execute(sql);
        logs  = cursor.fetchall()
        fieldName = cursor.description
       
        #setting the data into the dictionary 
        resultsList = []   
        for log in logs:
            result = {}
            i = 0
            while i < len(fieldName):
                result[fieldName[i][0]] = log[i]
                i = i+1    
            
            #adding the result into the dictionary 
            resultsList.append(result)
        
        #updating the job table with teh vistited = 1.
        Job.objects.filter(id = request.POST.get('datapost')).update(visited = 1)
        
        #returning the the respose to the file
        return render_to_response('misc/view_alert.html', {'alerts':resultsList}, context_instance = RequestContext(request))
    
def getroleId(request):
    """To show the list of roles and the server to assign
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """   

    try:
        
        #getting the roles from the list
        roles = NodeRole.objects.filter(node_id = request.POST.get('viewId'), assigned = True)
    
        #making the dictionary to save the data
        roleList = []
        
        #looping through the logs
        for role in roles:
            response_data = {}                     
            response_data["roleId"] = role.role_id
            roleList.append(response_data)      
                 
        #sending the response
        return HttpResponse(json.dumps(roleList), content_type = "application/json")
    except:
        raise Http404('Requested user not found.')

def optionsDetails(request):
    """
    To save the options and to manage the same.
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.     
    """
    message_value = 0
    
    #to show th form with values
    optionDetails = ThunderOptionValue.objects.filter(cloud_id = request.session['cloudId'])
    initialValue = {}
    
    #Iterating through the values to show into the form
    for optionDetail in optionDetails:
        initialValue[optionDetail.option.option_column] = optionDetail.option_value
        
    #setting the form values        
    forms = optionsForm(initial = initialValue) 
    
    # Creating the category dictionary
    categoryDic = collections.OrderedDict(sorted(optionCategoryList, key = itemgetter(0), reverse = False))
    
     
    #Checking the post 
    if request.method == 'POST':
    
        # Checks the access control, if not redirect
        if not checkFeatureAccess(request, 'edit_config'):
            return HttpResponseRedirect(settings.BASE_URL + "?notAuthenticated=1")
        
        #Setting the form with the posted values
        forms = optionsForm(request.POST)
        
        if not re.match(r'^[0-9a-zA-Z]*$', request.POST['defaultusername']):
            forms.errors['defaultusername'] = mark_safe('<ul class="errorlist"><li>Please give valid username.</li></ul>')
        else:
            
            #Getting the option values and deleting the same.
            ThunderOptionValue.objects.filter(cloud_id = request.session['cloudId']).delete()
           
            #Iteration through the post values
            for key in request.POST:
                
                try:
                    
                    #Getting the values
                    if key != 'csrfmiddlewaretoken':
                        
                        #getting the values from the thunder
                        thunderOption = ThunderOption.objects.get(option_column = key)
                        try:
                            
                            #Getting the values with item id
                            optionValue = ThunderOptionValue.objects.get(cloud_id = request.session['cloudId'], option_id = thunderOption.id)
                            
                            #updating to the database
                            if request.POST[key] != '':
                                optionValue.option_value = request.POST[key]
                                
                                #saving the values and assigning the message
                                optionValue.save()
                                message_value = 1
               
                        except ObjectDoesNotExist:
                            
                            #inserting to the database
                            if request.POST[key] != '':
                                ThunderOptionValue.objects.create(cloud_id = request.session['cloudId'], option_id = thunderOption.id, option_value = request.POST[key])
                                message_value = 2
                        
                except ThunderOption.DoesNotExist:
                    if key != 'csrfmiddlewaretoken':
                        messages.add_message(request, messages.ERROR, 'Option error.'+key) 
        
    #to show the message to the user
    if message_value == 1:
        messages.add_message(request, messages.SUCCESS, 'Option updated.')
    elif message_value == 2:
        messages.add_message(request, messages.SUCCESS, 'Option created.')
    
    #Returning the values
    return render_to_response('options/option_config.html', {'forms': forms, 'categoryLists': categoryDic}, context_instance = RequestContext(request))

def thunderAlertList(request):
    """
        To get the thunder alert
        Args:
            {
                request: Request from the cloud
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.
    """

    # To delete the selected alerts
    if request.method == 'POST':

        # Handles the request for alert list display.
        isViewAllRequest = request.POST.get('view-all', '')

        # getting the selected values from the list
        alertIds = request.POST.getlist('alertall[]')

        # To delete the alert from the log table
        for alertId in alertIds:
            Alert.objects.filter(pk = alertId).delete()

    else:

        # Handles the request for alert list display.
        isViewAllRequest = request.GET.get('view-all', '')

    # Getting only 5 latest alerts
    if not isViewAllRequest:
        alerts = Alert.objects.all().order_by("-id")[:5]

        # returning the the respose to the file
        return render_to_response('misc/thunder_alert.html', {'alerts':alerts}, context_instance = RequestContext(request))

    else:

        # Getting all alerts
        alerts = Alert.objects.all().order_by("-id")

        # returning the the respose to the file
        return render_to_response('misc/thunder_all_alerts.html', {'alerts':alerts}, context_instance = RequestContext(request))

def thunderAlertView(request):
    """To show the list of roles and the server to assign
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    #Checking the request is ajax or not, if ajax then limiting the result, else getting all
    if request.is_ajax():
      
        #Getting and updating the alert
        try:
            alertData = Alert.objects.filter(id = request.POST.get('datapost'))
            alertData.update(visited = 1)
            
        except Exception, e:
            print e
        
        #returning the the respose to the file
        return render_to_response('misc/thunder_view_alert.html', {'alerts':alertData}, context_instance = RequestContext(request))

def updateAlerts(request):
    """
        To update the the alert status to visited
    """

    # Setting the data variables
    responseData = {}
    status = True

    try:

        # Set the visited alerts
        Alert.objects.filter(visited = 0).update(visited = 1)
    except Exception, e:

        # Handles exception
        print e
        status = False

    # Sets the status to response data
    responseData["status"] = status

    # return the status
    return HttpResponse(json.dumps(responseData), content_type = "application/json")

def hasNewAlerts(request):
    """
        Function to check whether any new alerts are availabe.
    """

    # Checks whether any new alerts are there or not
    if Alert.objects.filter(visited = 0).exists():
        return HttpResponse(json.dumps({'hasNewAlerts' : True}), content_type = "application/json")
    else:
        return HttpResponse(json.dumps({'hasNewAlerts' : False}), content_type = "application/json")

@login_required
def updateNetworkCard(request):
    """To update the network card with the details
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    # Initialising the status
    errStatus = True

    #Checking the ajax
    if request.is_ajax():

        #Setting the counter and idlist
        counter = int(request.POST['count'])
        idList = request.POST['targetId'].split("sortable")

        #Checking the destination and updating the mapping
        if ((counter % 2) == 1):

            #Getting the network info
            mapIds = getMap(request.POST['ItemId'])
            cloudId = request.session.get('cloudId')
            networkInfo = NetworkDetails.objects.get(cloud_id = cloudId)
            
            #Looping through the mapped networkds
            for mapId in mapIds:
                
                #Gettign the vlan tags details
                haveVlan = getNetworkVlanTag(networkInfo, mapId.network_type)
                
                #Checking the storage network cidr is available, if not then we can assign it to any nic
                if (networkInfo.st_network_cidr == '' and mapId.network_type == 'S'):
                    NetworkInterfaceMapping.objects.filter(id = request.POST['ItemId']).update(nic = idList[1])
                    errStatus = False
                    return nodeConfig(request, request.POST.get("nodeId", ""), errStatus)
                
                #Checking the network have vlan or not.
                if haveVlan:
                    
                    #Checking the length, if it zero then updating the nic
                    NetworkInterfaceMapping.objects.filter(id = request.POST['ItemId']).update(nic = idList[1])
                    errStatus = False
                else:
                      
                    #If there is no network then updating the mapping.
                    mapData = NetworkInterfaceMapping.objects.filter(nic = idList[1])
                    if len(mapData) == 0:
                        errStatus = False
                        NetworkInterfaceMapping.objects.filter(id = request.POST['ItemId']).update(nic = idList[1])
                    else:
                        
                        #Looping through the mapped data
                        for map in mapData:
                            
                            #Getting the vlan tags of desitnation networks
                            haveTargetVlan = getNetworkVlanTag(networkInfo, map.network_type)
                            
                            #Checking the target vlan, if available then updating.
                            if haveTargetVlan:
                                errStatus = False
                                NetworkInterfaceMapping.objects.filter(id = request.POST['ItemId']).update(nic = idList[1])
                
    #returning the response to the html    
    return nodeConfig(request, request.POST.get("nodeId", ""), errStatus)

def roleProgress(nodeRoleId):
    """Function to get the progress of a role in a node
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns - progress data
        
    Raises:
        Exceptions and redirection to the login page.
    """
    try:
        
        #Getting the jobs from the table
        jobs = Job.objects.get(Q(subject_id = nodeRoleId) & Q(job_type = 'ROLE_ASSIGN'))
        return jobs.job_progress
    except Exception,e:
        return 0

def monitorCloud(request):
    """
    Function to check the process are running or not. Include zabbix, chef server
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns - details of the process
        
    Raises:
        Exceptions and redirection to the login page.
    
    """
    
    #setting the variables
    cobblerStatus = zabbixStatus = chefStatus = processList =  []
    
    #Getting the commands and name from the monitor table.
    services = MonitorService.objects.filter(status = True)
    
    #looping through the services
    for service in services:
        
        #Setting the list
        process = {}
        process['name'] = service.name
        
        try:
            
            #Running the command and getting the result from it
            processDetails = subprocess.check_output(service.command, shell = True).splitlines()
            process['servicename'] = processDetails
            process['status'] = 'success'
            alert_status = 'S'
        except subprocess.CalledProcessError as e:
            errorLog = "command '{}' return with error (code {}): {}" . format(e.cmd, e.returncode, e.output)
            process['servicename'] = errorLog.split(";")
            process['status'] = 'error'
            alert_status = 'F'
            
        #Setting the output
        processList.append(process)
        
        

        #parameters for the alert
        params = {'alert_type': service.name,
                  'referece_id':service.id,
                  'alert_content': 'Process with name ' + service.name + ' have the status as ' + process['status'], 
                  'alert_status' : alert_status
                  }
        
        #calling the function to add the alert
        thunderAlertAdd(params)
    
    #Sending to the template.
    return render_to_response('misc/monitor.html', {'process': processList}, context_instance = RequestContext(request))

#Including module for the reverse url resolver
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset
def reset(request):
    """
    Function to show the reset page
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns - html template
        
    Raises:
        Exceptions and redirection to the login page.
    
    """
    return password_reset(request, template_name='thunderadmin/reset_password.html',
        email_template_name='thunderadmin/reset_password.html',
        subject_template_name='thunderadmin/reset_subject.txt',
        post_reset_redirect=reverse('django.contrib.auth.views.login'))

def handler404(request):
    """
    Function to show custom page to handle 404
    Args:
        {
            request - request from the page
        }
    Returns:
            Returns - html template
    Raises:
        NA
    """
    
    #Setting the variable and template page for the 500 error
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    """
    Function to show custom page to handle 500
    Args:
        {
            request - request from the page
        }
    Returns:
        Returns - html template
    Raises:
        NA
    """
    
    #Setting the variable and template page for the 500 error
    response = render_to_response('500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response

def delSession(request):
    """
    To delete the session of the cloud
    Args:
        {
            request - request from the page
        }
    Returns:
        Returns - html template
    Raises:
        NA
    """
    if request.session.has_key('cloudId'):
        del(request.session['cloudId'])
    if request.session.has_key('cloudName'):
        del(request.session['cloudName'])