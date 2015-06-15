# @author: Geo Varghese
# @create_date: 4-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 4-Mar-2015
# @linking to other page: 
# @description: job urls mapping module

# importing required modules
from django.conf.urls import patterns, url

# url patterns mapping
urlpatterns = patterns(
    'job.actions',
    url(r'^([0-9]+)?\/$', 'execute_job', name='Execute Job'),
)
