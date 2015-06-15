# @author: Geo Varghese
# @create_date: 11-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 11-Mar-2015
# @linking to other page: 
# @description: deployment data bag functions

# importing required modules
import json
from cloud.common import *
from deployment.common import *
import pprint


def createDatabagValue(cloudId, jsonList, dataCatName):
    '''
    function to create databag json file and update it in databag
    cloudId   - The id of the cloud
    jsonList   - The json list of databag
    dataCatName   - The category name of databag
    Return - outputStr The output of the commands execution
    '''

    # create json json file
    from cloud.common import *
    dataBagJsonFile = CHEF_REPO_DIR + "/databags/databag" + str(cloudId) + ".json"
    f = open(dataBagJsonFile, 'w')
    f.write(json.dumps(jsonList))
    f.close()
        
    # execute chef commands to update the databag item
    from deployment.common import *
    chefCommand = "knife data bag from file " + getDataBagName(dataCatName, cloudId)
    chefCommand += " " + dataBagJsonFile + " --secret-file " + CHEF_SECRET_FILE
    outputStr = executeChefCommand(chefCommand)
    print "\n" + outputStr
    
    return outputStr


def updateDeploymentDataBags(cloudId):
    '''
    function to create data bag json and update the chef deployment server
    cloudId   - The id of the cloud
    Return - outputStr The output of the commands execution
    '''

    # create data bag lists
    from deployment.common import *
    createDataBagList(cloudId)

    # check cloud existing or not
    try:
        cloud = Cloud.objects.get(pk = cloudId)
    except Cloud.DoesNotExist:
        return "Cloud does not exist"
        
    # get cloud data bag values and update in chef server
    dbItemList = DataBagItem.objects.all()
    dataBagItemList = {}

    # get cloud data bag values for cloud and update in chef server
    dataBagVals = DataBag.objects.filter(cloud_id = cloudId)
    dataBagValsList = {}

    # loop through the db itemlist and create a dictionary with item id as key, if it contains data
    if len(dataBagVals) > 0:
        for item in dataBagVals:
            dataBagValsList[item.item_id] = item.databag_value

    # get default password of openstack default user
    overrideValList = getCloudOptions(cloudId)
    passwordColId = ThunderOption.objects.get(option_column = 'Default_Password').id
    passwordValue = overrideValList[passwordColId]
    usernameColId = ThunderOption.objects.get(option_column = 'defaultusername').id
    usernameValue = overrideValList[usernameColId]

    # if default password set then update in data bags
    if passwordValue and usernameValue:
        jsonList = {}
        jsonList['id'] = usernameValue
        jsonList[usernameValue] = passwordValue
        outputStr = createDatabagValue(cloudId, jsonList, "user_passwords")
    
    # To fetch the createDatabagValue o/p
    outputStr = ""
    
    # To get the databag values and create the databag
    for item in dbItemList:
        jsonList = {}
        dataCol = item.item_column

        # Checks if there is entry in databag table
        if dataBagValsList.has_key(item.id):
            dataVal = dataBagValsList[item.id]
        else:
            dataVal = item.default_value

        # Set the category name for the databag
        dataCatName = item.databag_category
        jsonList['id'] = dataCol
        jsonList[dataCol] = dataVal
        outputStr = createDatabagValue(cloudId, jsonList, dataCatName)
        
    return outputStr


def getDataBagName(dataCatName, cloudId):
    '''
    function to get data bag name
    cloudId   - The id of the cloud
    dataCatName   - The category name of databag
    @return Nam eof the data bag
    '''
    
    dataBagName = dataCatName + "_" + str(cloudId)
    return dataBagName


def createDataBagList(cloudId):
    '''
    function to create data bag list
    '''
    
    from deployment.common import *
    
    # loop through databag list cat names
    for listName, listLabel in dataBagCatList:
        chefCommand = "knife data bag create " + getDataBagName(listName, cloudId)
        outputStr = executeChefCommand(chefCommand)
        print "\n" + outputStr
