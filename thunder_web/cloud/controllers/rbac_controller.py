# Create your RBAC views and controls here.
# @author: Deepthy
# @created_date: 27-Jan-2015

# Including the modules
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from cloud.models import *
from django.template import Context
from django.contrib.auth import logout
from django.template import RequestContext
from requests.api import request
from django.contrib.auth.decorators import login_required
from django.db import connection
import json, datetime, random
from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint
from cloud.utils.thunder_features_role_map import *

class RBACController():
    """
        Class to manage the rbac functionalities
    """
    
    def getUserCloudAccess(self, userId):
        """
            To get the loggedin user's roles and privileges for the available clouds
        """
        
        # Variable initialisations
        userRoleList = []
        userCloudRoleMap = []
        userCloudAccess = {}
        roleResult = []
    
        # Defines the db cursor object 
        cursor = connection.cursor()
        
        # Fetch the user related role and permissions
        fetchRoleSql = "select user_role.user_id as user_id,role.name as role_name,role.id as role_id,role.domain_id as domain_id,permission.id as permission_id,permission.name as permission_name from thunder_user_role_mapping user_role,thunder_domain_role role,thunder_domain_role_permission permission where user_role.role_id=role.id and user_role.user_id=%d and role.permission_id=permission.id" % (int(userId))
        
        # Handling exception
        try:
            
            # Fetch the data
            cursor.execute(fetchRoleSql)
            roleResult = cursor.fetchall()
        
        except Exception, e:
            
            # Logs the exception
            print "Exception : ", e
            
        # Loop through each and assign to dictionary
        for roleUserId, roleName, roleId, domainId, permissionId, permissionName in roleResult:
            roleData = {}
            roleData['userId'] = int(roleUserId)
            roleData['roleName'] = roleName
            roleData['domainId'] = int(domainId)
            roleData['permissionId'] = int(permissionId)
            roleData['permissionName'] = permissionName
            roleData['roleId'] = int(roleId)
        
            # Appends the role data to list
            userRoleList.append(roleData)
            
        
        # Fetch the clouds associated with the role / permission
        for userRole in userRoleList:
            cloudList = []
            domainId = userRole['domainId']
            
            # checks if thunder or not and executes the fetch query
            if int(domainId) != 1:
                fetchCloudSql = "select cloud_id from thunder_cloud_domain_map where domain_id=%d" % (int(domainId))
            else:
                fetchCloudSql = "select id from thunder_cloud"
            cursor.execute(fetchCloudSql)
            userCloudMaps = cursor.fetchall()
            
            # Loop through the cloud map and appends to the list
            for cloud in userCloudMaps:
                cloudList.append(str(cloud[0]))
                
            # Sets the data
            userRole['cloudList'] = cloudList
            
            # Sets the privilege based access for the user
            userRole['featureAccess'] = roleFeatureMapping[permissionName]
            userCloudRoleMap.append(userRole)
#             userCloudAccess[str(userRole['roleId'])] = cloudList

        return {'userCloudRoleMap' : userCloudRoleMap}