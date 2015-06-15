# @author: Geo Varghese
# @create_date: 26-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 26-Mar-2015
# @linking to other page: 
# @description: deployment role functions

# importing required modules
import json
from cloud.common import *
from deployment.common import *


def updateObjectStorageRole():
    '''
    function to update object storage roles
    '''
   
    from cloud.common import * 
    roleList = ['os-object-storage-account', 'os-object-storage-container', 'os-object-storage-object']
    outputStr = ''

    # loop through the roles
    for role in roleList:
        roleFile = CHEF_REPO_DIR + "/roles/" + role + ".json"
        
        # update chef environment using the env file
        chefCommand = "knife role from file " + roleFile
        print "\nchef Command: " + chefCommand + "\n"
        from deployment.common import *
        outputStr += executeChefCommand(chefCommand)
    
    return outputStr
