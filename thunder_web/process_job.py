# @author: Geo Varghese
# @create_date: 6-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 6-Mar-2015
# @linking to other page: 
# @description: manage cron job module

# importing required modules
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thunder.settings")
 
# import cloud app
from cloud.models import *
from cloud.common import *
from job.actions import *

# get job list    
jobList = Job.objects.all().filter(
    Q(job_status = 'N') | Q(job_status = 'P'),
).order_by('job_priority', 'job_status', 'id')

print "\nStarted execution of manage job\n"

# if no jobs found
if not jobList:
    print "No jobs found to execute"    
else:
    
    # loop through job list
    for job in jobList:
        print "\nStarting job id: " + str(job.id) + "\n"
        print execute_job(job.id)