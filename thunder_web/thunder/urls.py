# Including the modules
from django.conf.urls import include, url
from django.contrib import admin
from cloud.views import *
from cloud.common import *
from cloud.rbac import *
from cloud.upgrade import *
import os.path
from thunderadmin.common import *
from django.views.generic import RedirectView

#to load the admin area.
admin.autodiscover()

#defining the site media path
site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

#defining the urls
urlpatterns = [
    url(r'^administrator/', include(admin.site.urls)),
    url(r'^$', index, name = 'index'),
    url(r'^user/(\w+)/$', user_page),
    url(r'^accounts/login/$', loginUser),
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    url(r'^login/$', login, name = 'loginUser'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': site_media }),
    url(r'^cloud/$', cloud, name='Cloud'),
    url(r'^cloudAdd/$', cloudAdd, name='CloudAdd'),
    url(r'^cloud/$', cloud),
    url(r'^cloud/(\w+)/$', cloudEdit, name='Cloud Edit'),
    url(r'^recipe/$', recipe),
    url(r'^feedsRecipe/(\w+)/$', feedsRecipe),  
    url(r'^roles/(\w+)$', roleList, name="AssignedRole"),
    url(r'^roleAssign/$', roleAssignment, name="roleAssignment"),
    url(r'^removeRole/$', removeRole, name="Remove Role"),
    url(r'^tabs/$', MainNavigationBaseTab.as_view(),  name="roleAssignmentss"),
    url(r'^support/$', supportTab,  name="support"),
    url(r'^log/$', logTab,  name="logs"),
    url(r'^nodeConfig/(\w+)$', nodeConfig,  name="nodeConfig"),
    url(r'^searchLogs/$', searchLogs,  name="searchLogs"), 
    url(r'^manageAddons/$', manageAddons,  name="manageAddons"),
    url(r'^api/', include('api.urls')),
    url(r'^clouds/', include('network.urls')),
    url(r'^admin/', include('thunderadmin.urls')),
    url(r'^job/', include('job.urls')),  
    url(r'^clouds/options', optionsDetails,  name="options"),  
    url(r'^clouds/task', taskDetails,  name='Task'),
    url(r'^clouds/insight', insight,  name='Insight'),
    # url(r'^cloud/config', configCloud,  name='createConfigFile'),
    url(r'^cloud/databag', dataBagConfig,  name='createConfigFile'),
    url(r'^cloud/alert', getLimitAlert,  name='getLimitAlert'),
    url(r'^cloud/jobView', jobView,  name='jobView'),
    url(r'^clouds/delete', deleteCloud,  name='deleteCloud'),
    url(r'^clouds/getroleId', getroleId,  name='getroleId'),
    url(r'^addCloudDomain', addCloudDomain,  name='addCloudDomain'),
    url(r'^addDomainRole', addDomainRole,  name='addDomainRole'),
    url(r'^addUser', addUser,  name='addUser'),
    url(r'^getDomainList', getDomainList, name = 'getDomainList'),
    url(r'^getRoleList', getRoleList,  name='getRoleList'),
    url(r'^deploythunder', deployThunder,  name='DeployThunder'),
    url(r'^download/', include('download.urls')),
    url(r'^deleteCloudDomain', deleteCloudDomain, name = 'deleteCloudDomain'),
    url(r'^deleteDomainRole', deleteDomainRole, name = 'deleteDomainRole'),
    url(r'^deleteRoleUser', deleteRoleUser, name = 'deleteRoleUser'),
    url(r'^thunderalert', thunderAlertList,  name='thunderAlert'),
    url(r'^alertView', thunderAlertView, name = 'thunderAlertView'),
    url(r'^updateNetworkCard/$', updateNetworkCard, name = "updateNetworkCard"),
    url(r'^monitor/$', monitorCloud, name = "monitorCloud"),
    url(r'^reset/$', 'cloud.views.reset', name='reset'),
    url(r'^updateAlerts/$', updateAlerts, name = 'updateAlerts'),
    url(r'^hasNewAlerts/$', hasNewAlerts, name = 'hasNewAlerts'),
    #url(r'^django-session-idle-timeout/', include('django-session-idle-timeout.urls')),
]

#adding the admin header part
admin.site.site_header = 'Thunder configuration'
