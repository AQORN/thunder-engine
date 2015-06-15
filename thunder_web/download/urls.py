# @author: Geo Varghese
# @create_date: 2-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 2-Apr-2015
# @linking to other page: 
# @description: download urls mapping module

# importing required modules
from django.conf.urls import patterns, url

# url patterns mapping
urlpatterns = patterns(
    'download.actions',
    url(r'^(.+)?\/$', 'downloadFile', name='Download File'),
)
