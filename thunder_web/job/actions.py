# @author: Geo Varghese
# @create_date: 4-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 4-Mar-2015
# @linking to other page: 
# @description: job action module

# importing required modules
from django.conf import settings
from rest_framework.test import APIClient
from django.http import HttpResponse, Http404
import json
from pprint import pprint
from cloud.common import *
from deployment.common import *
import datetime
from django.template.base import NodeList

# create api client object
client = APIClient()

def execute_job(jobId):
    """
    The function to execute job
    jobId - The id of the job
    """  
      
    # function call to get job details
    try:
        job = Job.objects.get(
            Q(id = jobId),
        )
    except Job.DoesNotExist:
        return "Job not found"
    
    # if job type is role assignment
    if job.job_status in ['N', 'P'] :
        nodeRoleAssignId = job.subject_id
        roleAssign = NodeRole.objects.get(pk = nodeRoleAssignId)
        nodeId = roleAssign.node_id
        role = Roletype.objects.get(pk = roleAssign.role_id)
        roleCode = role.role_code
        
        # check whether node is active
        nodeStatus = False
        try:
            nodeInfo = Nodelist.objects.get(id = nodeId)
            nodeStatus = isNodeActive(nodeInfo.host_name)
        except Exception, e:
            debugException(e)
        
        # if node is down
        if not nodeStatus:
            job.start_time = datetime.datetime.now()
            job.job_status = 'P'
            job.save()
            return HttpResponse("Error: Node is not active for deployment")
        
        # check job type and call corresponding API
        if job.job_type == 'ROLE_ASSIGN':
            deploymentAPILink = settings.API_URL + '/deployment/' + roleCode + '/' + str(nodeId) + '/'
        elif job.job_type == 'ROLE_REVOKE':
            deploymentAPILink = settings.API_URL + '/deployment/revoke/' + roleCode + '/' + str(nodeId) + '/'
        else:
            job.job_status = 'F'
            job.save()
            return HttpResponse("Error: Job process not defined")
        
    else:
        return HttpResponse("Job already completed")
     
    # update start time of job
    job.start_time = datetime.datetime.now()
    job.job_status = 'P'
    job.save()
     
    # call deployment api
    response = client.put(deploymentAPILink, {'job_id': jobId}, format = 'json')
    parser = json.loads(response.content)
    
    # check whether cron job is success
    if parser['status'] == 'Error':
        print "\nJob Failed Error: " + parser['errorMsg'] + "\n"
    else:
        print "\nJob successfully completed\n"
    
    return parser