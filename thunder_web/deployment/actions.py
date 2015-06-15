# @author: Geo Varghese
# @create_date: 2-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 2-Mar-2015
# @linking to other page: 
# @description: deployment action module

# importing required modules
from deployment.common import *

@api_view(['PUT'])
def deploy_controller(request, nodeId):
    """
    function to deploy the controller role
    request - PUT - Deploy controller
    nodeId - The id of the node
    """

    roleCode = 'controller'

    # check for valid node id
    try:
        node = Nodelist.objects.get(pk = nodeId)
    except Nodelist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # check for request method
    if request.method == 'PUT':
    
        # get role details and recipie list
        role = Roletype.objects.get(role_code = roleCode);
        recipeList = Recipe.objects.all().filter(roletype_id = role.id, status = 1).order_by("priority").order_by("id")
            
        jobId = request.data['job_id']
        recipePrList = collections.OrderedDict()
        
        # loop through recipie list  
        for recipe in recipeList:
            
            # check whether priority key set or not 
            if not recipePrList.has_key(recipe.priority) :
                recipePrList[recipe.priority] = []
            
            # append recipe to priority list
            recipePrList[recipe.priority].append(recipe)    
                
        # deploy role to node
        outputInfo = deployRoleToNode(node, recipePrList, jobId, roleCode)        
        return Response(outputInfo)
    
    else:
        return Response({'status': "Error", 'errorMsg': "PUT Request method only accepted"})
    

@api_view(['PUT'])
def deploy_compute(request, nodeId):
    """
    function to deploy the compute role
    request - PUT - Deploy compute
    nodeId - The id of the node
    """

    roleCode = 'compute'

    # check for valid node id
    try:
        node = Nodelist.objects.get(pk = nodeId)
    except Nodelist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # check for request method
    if request.method == 'PUT':
    
        # get role details and recipie list
        role = Roletype.objects.get(role_code = roleCode);
        recipeList = Recipe.objects.all().filter(roletype_id = role.id, status = 1).order_by("priority").order_by("id")
        jobId = request.data['job_id']
        recipePrList = collections.OrderedDict()
        
        # loop through recipie list  
        for recipe in recipeList:
            
            # check whether priority key set or not 
            if not recipePrList.has_key(recipe.priority) :
                recipePrList[recipe.priority] = []
            
            # append recipe to priority list
            recipePrList[recipe.priority].append(recipe)    
                
        # deploy role to node
        outputInfo = deployRoleToNode(node, recipePrList, jobId, roleCode)        
        return Response(outputInfo)
    
    else:
        return Response({'status': "Error", 'errorMsg': "PUT Request method only accepted"})
    

@api_view(['PUT'])
def deploy_block_storage(request, nodeId):
    """
    function to deploy the block storage role
    request - PUT - Deploy block storage
    nodeId - The id of the node
    """

    roleCode = 'block_storage'

    # check for valid node id
    try:
        node = Nodelist.objects.get(pk = nodeId)
    except Nodelist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # check for request method
    if request.method == 'PUT':
    
        # get role details and recipie list
        role = Roletype.objects.get(role_code = roleCode);
        recipeList = Recipe.objects.all().filter(roletype_id = role.id, status = 1).order_by("priority").order_by("id")
            
        jobId = request.data['job_id']
        recipePrList = collections.OrderedDict()
        
        # loop through recipie list  
        for recipe in recipeList:
            
            # check whether priority key set or not 
            if not recipePrList.has_key(recipe.priority) :
                recipePrList[recipe.priority] = []
            
            # append recipe to priority list
            recipePrList[recipe.priority].append(recipe)    
                
        # deploy role to node
        outputInfo = deployRoleToNode(node, recipePrList, jobId, roleCode)        
        return Response(outputInfo)
    
    else:
        return Response({'status': "Error", 'errorMsg': "PUT Request method only accepted"})
    

@api_view(['PUT'])
def deploy_object_storage(request, nodeId):
    """
    function to deploy the object storage role
    request - PUT - Deploy object storage
    nodeId - The id of the node
    """

    roleCode = 'object_storage'

    # check for valid node id
    try:
        node = Nodelist.objects.get(pk = nodeId)
    except Nodelist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # check for request method
    if request.method == 'PUT':
    
        # get role details and recipie list
        role = Roletype.objects.get(role_code = roleCode);
        recipeList = Recipe.objects.all().filter(roletype_id = role.id, status = 1).order_by("id").order_by("priority")
            
        jobId = request.data['job_id']
        recipePrList = collections.OrderedDict()
        
        # loop through recipie list  
        for recipe in recipeList:
            
            # check whether priority key set or not 
            if not recipePrList.has_key(recipe.priority) :
                recipePrList[recipe.priority] = []
            
            # append recipe to priority list
            recipePrList[recipe.priority].append(recipe)    
                
        # deploy role to node
        outputInfo = deployRoleToNode(node, recipePrList, jobId, roleCode)        
        return Response(outputInfo)
    
    else:
        return Response({'status': "Error", 'errorMsg': "PUT Request method only accepted"})
    

@api_view(['PUT'])    
def deployRevokeRole(request, roleCode, nodeId):
    """
    function to revoke roles from nodes.
    request - PUT - revoke request
    roleCode - The role code to revoke
    nodeId - The id of the node
    """
    
    # check for valid node id
    try:
        node = Nodelist.objects.get(pk = nodeId)
    except Nodelist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # check for request method
    if request.method == 'PUT':
        
        jobId = request.data['job_id']
        
        # revoke node role
        outputInfo = deployRevokeNodeRole(node, jobId, roleCode)        
        return Response(outputInfo)
        
    else:
        return Response({'status': "Error", 'errorMsg': "PUT Request method only accepted"})