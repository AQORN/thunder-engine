# @author: Geo Varghese
# @create_date: 2-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 2-Mar-2015
# @linking to other page: 
# @description: app urls mapping module

# importing required modules
from django.conf.urls import patterns, url

# url patterns mapping
urlpatterns = patterns(
    'deployment.actions',
    url(r'^controller/([0-9]+)?\/$', 'deploy_controller', name='Deploy Controller'),
    url(r'^compute/([0-9]+)?\/$', 'deploy_compute', name='Deploy Compute'),
    url(r'^block_storage/([0-9]+)?\/$', 'deploy_block_storage', name='Deploy Block Storage'),
    url(r'^object_storage/([0-9]+)?\/$', 'deploy_object_storage', name='Deploy Object Storage'),
    url(r'^revoke/(.+)/([0-9]+)?\/$', 'deployRevokeRole', name='Revoke role'),
)
