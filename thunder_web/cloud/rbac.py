# Create your RBAC views and controls here.
# @author: Deepthy
# @created_date: 23-Jan-2015

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

# Importing the api client
from rest_framework.test import APIClient
from pprint import pprint
from django.db import connection
import numbers
from django.core.validators import validate_email
from django.db.models import Q
from cloud.utils.decorators import checkFeatureAccess
from cloud.controllers.rbac_controller import *

# Setting the base url
APIURL = settings.BASE_URL

class MainNavigationBaseTab(TabView):
    """ Base class for all main navigation tabs. """
    
    tab_group = 'main_navigation'
    tab_classes = ['main-navigation-tab']
    template_name='tab/index.html'

    def cloudList(self):
        """
            Function to fetch the cloud list available in the thunder
        """
        
        # Making the dictionary to save the data
        cloudList = []
        
        try:
            
            # Get the cloud and role for the user
            rbacController = RBACController()
            cloudAccessMapData = rbacController.getUserCloudAccess(self.request.user.id)
            cloudAccessMap = cloudAccessMapData['userCloudRoleMap'][0]
            userCloudList = cloudAccessMap['cloudList']

            # Fetch all the available clouds
            if len(userCloudList) > 0:

                # Fetch the cloud list from session
                availableCloudList = ','.join(userCloudList)
                thunderClouds = Cloud.objects.extra(where = ["id in (%s)" % (str(availableCloudList))])
            else:
                thunderClouds = Cloud.objects.all()
            
            # Looping through the clouds
            for cloud in thunderClouds:
                responseData = {}  
                responseData['id'] =  int(cloud.id)
                responseData['name'] =  cloud.cloud_name
                cloudList.append(responseData)  
            
            # Return the cloud list
            return cloudList
        
        except Exception, e:
            print e
            return cloudList
    
    def domainCloudList(self):
        """
            Function to fetch the cloud domain list available in the thunder
        """
        
        try:

            # Create the cursor object
            cursor = connection.cursor()

            # Fetch the domain objects (get all domains for the thunder domain)
            if self.request.session['cloudAccessMapData']['domainId'] == 1:
                fetchQuery = "select id, name from thunder_cloud_domain"
                cursor.execute(fetchQuery)
                domainList = cursor.fetchall()
            else:

                # Get the cloud and role for the user
                rbacController = RBACController()
                cloudAccessMapData = rbacController.getUserCloudAccess(self.request.user.id)
                cloudAccessMap = cloudAccessMapData['userCloudRoleMap'][0]
                userCloudList = cloudAccessMap['cloudList']

                # Fetch query for domain list
                cloudList = ','.join(userCloudList)
                fetchQuery = "select distinct domain.id as id,domain.name as name from thunder_cloud cloud,thunder_cloud_domain domain,thunder_cloud_domain_map cloud_domain where cloud.id=cloud_domain.cloud_id and domain.id=cloud_domain.domain_id and cloud.id in (%s)" % (str(cloudList))
                cursor.execute(fetchQuery)
                domainList = cursor.fetchall()

            # Initialising
            domainCloudList = []
            
            # Loops through all the domains to get the clouds related to it
            for id, name in domainList:
                
                # Create the cursor object to fetch the cloud details 
                cursor.execute("select cloud_name,cloud_id from thunder_cloud_domain_map domain_map, thunder_cloud cloud where cloud.id=domain_map.cloud_id and domain_id=%d" % (int(id)))
                cloudDomainMaps = cursor.fetchall()
                cloudNameStr = ""
                
                # Looping through the clouds
                for cloudName, cloudId in cloudDomainMaps:
                    cloudNameStr =  cloudNameStr + ", " + str(cloudName)
                
                # Strips the unwanted comma
                cloudNameStr = cloudNameStr.strip(',')
                
                # For main domain
                if len(cloudNameStr) == 0 and (id) == 1:
                    cloudNameStr = "Everything"
                
                # Creates response object data
                responseData = {}
                responseData['domain_name'] = name
                responseData['domain_id'] = id
                responseData['cloud_name'] = cloudNameStr
                domainCloudList.append(responseData)

            # Returns the domain cloud list association           
            return domainCloudList
        except Exception, e:
            print e
            
    def rolePermissionList(self):
        """
            Function to fetch the role permissions from db
        """
        
        # Making the dictionary to save the data
        rolePermissionList = []
        
        try:
            
            # Fetch all the available role permissions
            rolePermissions = DomainRolePermission.objects.all()
            
            # Looping through the role permissions
            for permission in rolePermissions:
                responseData = {}  
                responseData['id'] =  int(permission.id)
                responseData['name'] =  permission.name
                responseData['description'] =  permission.description
                rolePermissionList.append(responseData)  
            
            # Return the role permission list
            return rolePermissionList
        
        except Exception, e:
            print e
            return rolePermissionList
    
    def domainList(self):
        """
            Function to fetch the domain list available in the thunder
        """
        
        # Making the dictionary to save the data
        domainList = []

        try:

            # Create the cursor object
            cursor = connection.cursor()

            # Fetch the domain details
            fetchQuery = "select distinct domain.id as id,domain.name as name from thunder_cloud cloud,thunder_cloud_domain domain,thunder_cloud_domain_map cloud_domain where cloud.id=cloud_domain.cloud_id and domain.id=cloud_domain.domain_id"
            cursor.execute(fetchQuery)
            thunderDomains = cursor.fetchall()

            # Looping through the domains
            for id, name in thunderDomains:
                responseData = {}
                responseData['id'] = int(id)
                responseData['name'] = name
                domainList.append(responseData)
            
            # Return the domain list
            return domainList
        
        except Exception, e:
            print e
            return domainList
        
        
    def domainRoles(self):
        """
            Function to fetch the details of the domain roles to display in the role tab.
        """
    
        # Create the cursor object to fetch the cloud details 
        cursor = connection.cursor()

        # Creating list dictionary
        domainRoleList = []
        
        try:
        
            # Fetching the details
            fetchQuery = "select role.name as role_name,domain.name as domain_name, domain.id as domain_id, permission.name as permission_name,role.id as role_id from thunder_domain_role role, thunder_cloud_domain domain, thunder_domain_role_permission permission where role.domain_id=domain.id and role.permission_id=permission.id"
            cursor.execute(fetchQuery)
            domainRoles = cursor.fetchall()
            
            # Looping through the roles
            for role_name, domain_name, domain_id, permission_name, role_id in domainRoles:
                responseData = {}
                responseData['role'] = role_name
                responseData['domain'] = domain_name
                responseData['domain_id'] = domain_id
                responseData['permission'] = permission_name
                responseData['role_id'] = role_id
                domainRoleList.append(responseData)
                
            # Return the domain list
            return domainRoleList
        
        except Exception, e:
            print e
            return domainRoleList
            
    
    def userRoles(self):
        """
            To fetch the user and associated role details
        """     
    
        # Create the cursor object to fetch the cloud details 
        cursor = connection.cursor()

        # Creating list dictionary
        userRoleList = []

        try:

            # Query to fetch the data
            fetchQuery = "select user.username as user_name, domain_role.name as role_name,user_role.role_id as role_id, user.id as user_id from auth_user user, thunder_user_role_mapping user_role, thunder_domain_role domain_role where user_role.user_id=user.id and domain_role.id=user_role.role_id"
            cursor.execute(fetchQuery)
            userRoles = cursor.fetchall()

            # Looping through the roles
            for user_name, role_name, role_id, user_id in userRoles:
                responseData = {}  
                responseData['user'] = user_name
                responseData['role'] = role_name
                responseData['role_id'] = role_id
                responseData['user_id'] = user_id
                userRoleList.append(responseData)

            # Return the domain list
            return userRoleList

        except Exception, e:
            print e
            return userRoleList

    def get_context_data(self, **kwargs):
        """
            Overriding context of super class
        """

        # Overriding context of super class
        context = super(MainNavigationBaseTab, self).get_context_data(**kwargs)
        return context

    @property
    def tab_classes(self):
        """ 
            If user is logged in, set ``logged_in_only`` class
        """

        # Super class available tab classes
        classes = super(MainNavigationBaseTab, self).tab_classes[:]

        #adding the class
        if self.current_tab.request.user.is_authenticated():
            classes += ['logged_in_only']
        return classes

class DomainTab(MainNavigationBaseTab):
    """ Domain TabView is only visible after authentication. """

    # Tab specific field values
    _is_tab = True
    tab_id = 'domain_tab'
    tab_label = _('Domains')
    tab_classes = 'domain'
    tab_rel = 'nofollow,noindex'
    template_name = 'tab/domain_tab.html'
    
    def get_context_data(self, **kwargs):
        """
         Overriding the context
        """

        # Super class context object
        context = super(DomainTab, self).get_context_data(**kwargs)

        # Fetch the cloud list from thunder
        cloudList = getClouds()
        context['spam'] = 'ham123'
        context['cloudList'] = cloudList

        return context

class RolesTab(MainNavigationBaseTab):
    """ Roles TabView is only visible after authentication """

    # Tab specific field values
    _is_tab = True
    tab_id = 'roles_tab'
    tab_label = _('Roles')
    tab_classes = 'roles'
    tab_rel = 'nofollow,noindex'
    template_name = 'tab/roles_tab.html'

class UserTab(MainNavigationBaseTab):
    """ User TabView class """
    
    # Tab specific field values
    _is_tab = True
    tab_id = 'users_tab'
    tab_label = _('Users')
    tab_classes = 'user'
    template_name = 'tab/user_tab.html'

def addCloudDomain(request):
    """
        Function to add the domain for the cloud selected
    """

    # Executes if the add domain request is requested
    if request.method == "POST":

        # Fetching the post data
        domainName = str(request.POST['domainName']).strip()
        cloudListString = str(request.POST['cloudList'])
        status = True

        # Setting the dictionary        
        responseData = {}

        # Checks if cloud is selected or not
        if len(cloudListString) == 0:

            #To show the message to the user 
            status = False
            responseData['message_scope'] = "Select a cloud"
        else:

            # Splits and creates the list of clouds selected.
            cloudList = cloudListString.split(',')
            responseData['message_scope'] = ""

        # Checks if domain is null
        if len(domainName) == 0:

            #To show the message to the user 
            status = False
            responseData['message_domain'] = "Enter domain name"
        else:

            # Sets the error message
            responseData['message_domain'] = ""

        if not status:

            # Set the request status
            responseData['status'] = status

            # Sending the response
            return HttpResponse(json.dumps(responseData), content_type = "application/json")

        try:

            # Cursor object for db connection
            cursor = connection.cursor()

            # Checks for existence of the domain
            cursor.execute("select * from thunder_cloud_domain where name='%s'" % (domainName))
            domains = cursor.fetchall()    

            # Executed only if the domain is not already existing
            if len(domains) == 0:

                # Creates domain object
                newDomainObj = CloudDomain()
                newDomainObj = CloudDomain.objects.create(name = domainName)
                newDomainId = newDomainObj.id

                # Creates mapping entries for the clouds associated
                for counter in range(0, len(cloudList)):
                    cloudId = cloudList[counter]
                    CloudDomainMap.objects.create(cloud = Cloud(cloudId), domain = CloudDomain(newDomainObj.id))

                # Create the cursor object to fetch the cloud details 
                cursor.execute("select cloud_name from thunder_cloud where id IN (%s)" % (cloudListString))
                cloudNameList = cursor.fetchall()
                cloudNameStr = ""

                # Looping through the clouds
                for cloudName in cloudNameList:
                    cloudNameStr =  cloudNameStr + ", " + str(cloudName[0])

                # Strips the unwanted comma
                cloudNameStr = cloudNameStr.strip(',')

                # Set response data
                responseData['domainName'] = domainName
                responseData['cloudNameStr'] = cloudNameStr
                responseData['domainId'] = int(newDomainId)

                # To show the message to the user 
                status = True

            else:

                #To show the message to the user 
                status = False
                responseData['message_domain'] = "Domain already exists"

        except Exception, e:

            #To show the message to the user 
            status = False

        # Set the request status
        responseData['status'] = status

        # Sending the response
        return HttpResponse(json.dumps(responseData), content_type = "application/json")

def addDomainRole(request):
    """
        Function to handle the domain role add
    """

    # Executes if it is a post request
    if request.method == "POST":

        # Sets the post value
        roleName = str(request.POST['role_name']).strip()
        domainIdValue = request.POST['domain_list']
        permissionIdValue = request.POST['permission_list']
        status = True
        responseData = {}

        # Sets error messages for validation of fields
        if len(roleName) == 0:

            #To show the message to the user 
            responseData['message_role'] = "Enter a role name"
            status = False
        else:

            # Resets the error message
            responseData['message_role'] = ""

        # Sets error messages for validation of fields
        if not domainIdValue.isdigit():

            #To show the message to the user 
            responseData['message_domain'] = "Select a domain"
            status = False
        else:

            # Resets the error message
            responseData['message_domain'] = ""

        # Sets error messages for validation of fields
        if not permissionIdValue.isdigit():

            #To show the message to the user 
            responseData['message_permission'] = "Select a permission"
            status = False
        else:

            # Resets the error message
            responseData['message_permission'] = ""

        if not status:

            # Set the request status
            responseData['status'] = status
            
            # Sending the response
            return HttpResponse(json.dumps(responseData), content_type = "application/json")

        try:

            # Cursor object for db connection
            cursor = connection.cursor()

            # Checks for existence of the domain
            cursor.execute("select * from thunder_domain_role where name='%s'" % (roleName))
            roles = cursor.fetchall()   

            # Executed only if the domain is not already existing
            if len(roles) == 0:

                # Creates new role object
                newRoleObj = DomainRole()
                newRoleObj = DomainRole.objects.create(name = roleName, domain = CloudDomain(int(domainIdValue)), permission = DomainRolePermission(int(permissionIdValue)))
                newRoleId = newRoleObj.id

                # Set the response data
                responseData['roleName'] = roleName 
                responseData['permissionName'] = str(request.POST['permissionText']) 
                responseData['domainName'] =  str(request.POST['domainText'])
                responseData['roleId'] = int(newRoleId)
            else:

                #To show the message to the user 
                status = False
                responseData['message_role'] = "Role already exists"

        except Exception, e:

            #To show the message to the user 
            status = False

        # Set the request status
        responseData['status'] = status

        # Sending the response
        return HttpResponse(json.dumps(responseData), content_type = "application/json")

def addUser(request):
    """
        Creates a django user account
    """

    # Executes if it is a post request
    if request.method == "POST":

        # Fetch the post data
        accountName = str(request.POST['account_name']).strip()
        userName = str(request.POST['user_name']).strip()
        password = str(request.POST['password']).strip()
        email = str(request.POST['email']).strip()
        roleName = str(request.POST['roleText']).strip()
        roleIdValue = request.POST['role_list']
        status = True
        responseData = {}

        # Sets error messages for validation of fields
        if len(accountName) == 0:

            #To show the message to the user 
            responseData['message_account'] = "Enter account name"
            status = False
        else:

            # Resets the error message
            responseData['message_account'] = ""

        # Sets error messages for validation of fields
        if len(userName) == 0:

            #To show the message to the user 
            responseData['message_user'] = "Enter user name"
            status = False
        else:

            # Resets the error message
            responseData['message_user'] = ""

        # Sets error messages for validation of fields
        if len(password) == 0 or len(password) < 6:

            #To show the message to the user 
            responseData['message_password'] = "Password should have atleast 6 characters"
            status = False
        else:

            # Resets the error message
            responseData['message_password'] = ""

        # Sets error messages for validation of fields
        try:

            validate_email(email)

            # Resets the error message
            responseData['message_email'] = ""
        except Exception, e:

            #To show the message to the user 
            responseData['message_email'] = "Enter a valid email"
            status = False

        # Sets error messages for validation of fields
        if not roleIdValue.isdigit():

            #To show the message to the user 
            responseData['message_role'] = "Select a role"
            status = False
        else:

            # Resets the error message
            responseData['message_role'] = ""

        if not status:

            # Set the request status
            responseData['status'] = status

            # Sending the response
            return HttpResponse(json.dumps(responseData), content_type = "application/json")

        try:

            # Checks for existence of the domain
            try:

                # Gets the user object
                user = User.objects.get(username = userName)

                #To show the message to the user 
                status = False
                responseData['message_user'] = "User name already exists"

            except Exception, e:

                # Creates user object and maps to the role
                newUser = User.objects.create_user(username = userName, email = email, password = password)
                newUserId = newUser.id
                UserRoleMap.objects.create(user = User(newUser.id), role = DomainRole(int(roleIdValue)))

                # Set the response data
                responseData['roleName'] = roleName 
                responseData['userName'] = userName
                responseData['userId'] = int(newUserId)

        except Exception, e:

            #To show the message to the user 
            status = False

        # Set the request status
        responseData['status'] = status

        # Sending the response
        return HttpResponse(json.dumps(responseData), content_type = "application/json")

def getDomainList(request):
    """
        Get the domain list
    """

    # Declaration
    responseData = {}
    domainList = []
    allDomainList = []
    roleList = []

    # Create the cursor object
    cursor = connection.cursor()

    try:

        # Created object and fetch object list
        navigationTabObj = MainNavigationBaseTab()
        allDomainList = navigationTabObj.domainList()

        # Created object and fetch object list
        allRoleList = navigationTabObj.domainRoles()

        # Checks if thunder user
        if request.session['cloudAccessMapData']['domainId'] == 1:
            domainList = allDomainList
            # roleList = filter(lambda d: d['role_id'] >= 1, allRoleList)
            roleList = allRoleList
        else:

            # Get the cloud and role for the user
            rbacController = RBACController()
            cloudAccessMapData = rbacController.getUserCloudAccess(request.user.id)
            cloudAccessMap = cloudAccessMapData['userCloudRoleMap'][0]
            userCloudList = cloudAccessMap['cloudList']

            # Fetch query to get domain list
            cloudList = ','.join(userCloudList)
            fetchQuery = "select distinct domain.id as id,domain.name as name from thunder_cloud cloud,thunder_cloud_domain domain,thunder_cloud_domain_map cloud_domain where cloud.id=cloud_domain.cloud_id and domain.id=cloud_domain.domain_id and cloud.id in (%s)" % (str(cloudList))
            cursor.execute(fetchQuery)
            domains = cursor.fetchall()
            domainStr = ""

            # Create the domain list
            for id, name in domains:
                domainData = {}
                domainData['name'] = name
                domainData['id'] = id
                domainStr = domainStr + "," + str(id)
                domainList.append(domainData)

            # Fetch the corresponding roles
            domainStr = domainStr.strip(',')
            fetchQuery = "select role.name as role_name,domain.name as domain_name, domain.id as domain_id, permission.name as permission_name,role.id as role_id from thunder_domain_role role, thunder_cloud_domain domain, thunder_domain_role_permission permission where role.domain_id=domain.id and role.permission_id=permission.id and domain.id IN (%s)" % (domainStr)
            cursor.execute(fetchQuery)
            domainRoles = cursor.fetchall()

            # Looping through the roles
            for role_name, domain_name, domain_id, permission_name, role_id in domainRoles:
                roleData = {}
                roleData['role'] = role_name
                roleData['domain'] = domain_name
                roleData['domain_id'] = domain_id
                roleData['permission'] = permission_name
                roleData['role_id'] = role_id
                roleList.append(roleData)

        responseData['status'] = True

    except Exception, e:

        #To show the message to the user 
        responseData['status'] = False

    # Sets the result to response object
    responseData['domainList'] = domainList
    responseData['roleList'] = roleList

    # Sending the response
    return HttpResponse(json.dumps(responseData), content_type = "application/json")
    
def getRoleList(request):
    """
        Get the role list
    """

    # Declaration
    responseData = {}
    roleList = []
    allRoleList = []
    domainList = []
    allDomainList = []
    userList = []

    # Create the cursor object
    cursor = connection.cursor()

    try:

        # Created object and fetch object list
        navigationTabObj = MainNavigationBaseTab()
        allRoleList = navigationTabObj.domainRoles()

        # Query to fetch the user role data
        fetchUserQuery = "select user.username as user_name, domain_role.name as role_name,user_role.role_id as role_id, user.id as user_id from auth_user user, thunder_user_role_mapping user_role, thunder_domain_role domain_role where user_role.user_id=user.id and domain_role.id=user_role.role_id"

        # Checks if thunder user
        if request.session['cloudAccessMapData']['roleId'] == 1:

            # Get the role which is not of the root role
            roleList = filter(lambda d: d['role_id'] > 1, allRoleList)
        else:

            # Get the cloud and role for the user
            rbacController = RBACController()
            cloudAccessMapData = rbacController.getUserCloudAccess(request.user.id)
            cloudAccessMap = cloudAccessMapData['userCloudRoleMap'][0]
            userCloudList = cloudAccessMap['cloudList']

            # Fetch query to get domain list
            cloudList = ','.join(userCloudList)
            fetchQuery = "select distinct domain.id as id,domain.name as name from thunder_cloud cloud,thunder_cloud_domain domain,thunder_cloud_domain_map cloud_domain where cloud.id=cloud_domain.cloud_id and domain.id=cloud_domain.domain_id and cloud.id in (%s)" % (str(cloudList))
            cursor.execute(fetchQuery)
            domains = cursor.fetchall()
            domainStr = ""

            # Creates the domain list
            for id, name in domains:
                domainData = {}
                domainData['name'] = name
                domainData['id'] = id
                domainStr = domainStr + "," + str(id)
                domainList.append(domainData)

            # Fetch the corresponding roles
            domainStr = domainStr.strip(',')
            fetchQuery = "select role.name as role_name,domain.name as domain_name, domain.id as domain_id, permission.name as permission_name,role.id as role_id from thunder_domain_role role, thunder_cloud_domain domain, thunder_domain_role_permission permission where role.domain_id=domain.id and role.permission_id=permission.id and domain.id IN (%s)" % (domainStr)
            cursor.execute(fetchQuery)
            domainRoles = cursor.fetchall()
            roleStr = ""

            # Looping through the roles
            for role_name, domain_name, domain_id, permission_name, role_id in domainRoles:
                roleData = {}
                roleData['role'] = role_name
                roleData['domain'] = domain_name
                roleData['domain_id'] = domain_id
                roleData['permission'] = permission_name
                roleData['role_id'] = role_id
                roleStr = roleStr + "," + str(role_id)
                roleList.append(roleData)

            # Fetch query for roles
            roleStr = roleStr.strip(',')
            fetchUserQuery = fetchUserQuery + " and user_role.role_id in (%s)" % (roleStr)

        # Fetch user data
        cursor.execute(fetchUserQuery)
        userRoles = cursor.fetchall()

        # Looping through the roles
        for user_name, role_name, role_id, user_id in userRoles:
            userData = {}
            userData['user'] = user_name
            userData['role'] = role_name
            userData['role_id'] = role_id
            userData['user_id'] = user_id
            userList.append(userData)

        responseData['status'] = True

    except Exception, e:

        #To show the message to the user 
        responseData['status'] = False
        print e

    # Sets the result to response object
    responseData['roleList'] = roleList
    responseData['userList'] = userList

    # Sending the response
    return HttpResponse(json.dumps(responseData), content_type = "application/json")

def getDomainRoles(domainId, onlyIds = False):
    """
        Get the role list of the domain
    """

    # Initialise the data variable
    domainRoleList = []
    domainRoleIdList = []

    # Fetch the domain roles for the domain
    domainRoles = DomainRole.objects.filter(domain = CloudDomain(int(domainId)))

    # Create the role list
    for roles in domainRoles:
        rolesData = {}
        rolesData['id'] = roles.id
        rolesData['name'] = roles.name
        domainRoleList.append(rolesData)
        domainRoleIdList.append(roles.id)

    # Checks if only id list need to be returned
    if onlyIds:
        return domainRoleIdList
    else:
        return domainRoles

def getRolesUsers(roleId):
    """
        Get the user list of the role
    """

    # Initialise the data variable
    roleUserList = []
    roleUserIdList = []

    # Fetch the domain roles for the domain
    roleUsers = UserRoleMap.objects.filter(role = DomainRole(int(roleId)))

    # Create the user list
    for users in roleUsers:
        roleUserIdList.append(users.id)

    return roleUserIdList

def deleteCloudDomain(request):
    """
        Function to delete the domain and the associated roles and users
    """

    # Initializing the data variables
    domainId = str(request.POST['domainId']).strip()
    responseData = {}

    try:

        # Get roles data related to domain
        roles = getDomainRoles(domainId, True)
        userList = []

        # Fetch the domain roles users for the domain
        roleUsers = UserRoleMap.objects.filter(role__in = roles).values('user').distinct()
        for user in roleUsers:
            userList.append(int(user['user']))

        # Performs the cloud domain delete functionality
        returnStatus = CloudDomain.objects.filter(id = int(domainId)).delete()

        # Deletes the users related to the roles / domain
        User.objects.filter(id__in = userList).delete()

        # To show the message to the user
        responseData['status'] = True
    except Exception, e:

        print "Exception : ", e

        # To show the message to the user
        responseData['status'] = False

    # Sending the response
    return HttpResponse(json.dumps(responseData), content_type = "application/json")

def deleteDomainRole(request):
    """
        Delete the role and associated users
    """

    # Initializing the data variables
    roleId = str(request.POST['roleId']).strip()
    responseData = {}

    try:

        # Get user data related to role
        users = getRolesUsers(roleId)
        userList = []

        # Fetch the domain roles users for the domain
        for userId in users:
            userList.append(int(userId))

        # Performs the cloud role  delete functionality
        returnStatus = DomainRole.objects.filter(id = int(roleId)).delete()

        # Deletes the users related to the role
        User.objects.filter(id__in = userList).delete()

        # To show the message to the user
        responseData['status'] = True
    except Exception, e:

        print "Exception : ", e

        # To show the message to the user
        responseData['status'] = False

    # Sending the response
    return HttpResponse(json.dumps(responseData), content_type = "application/json")

def deleteRoleUser(request):
    """
        Delete the user
    """

    # Initializing the data variables
    userId = str(request.POST['userId']).strip()
    responseData = {}

    try:

        # Performs the cloud user delete functionality
        returnStatus = User.objects.filter(id = int(userId)).delete()

        # To show the message to the user
        responseData['status'] = True
    except Exception, e:

        print "Exception : ", e

        # To show the message to the user
        responseData['status'] = False

    # Sending the response
    return HttpResponse(json.dumps(responseData), content_type = "application/json")