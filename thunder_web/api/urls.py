from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    'api.views',
    url(r'^tasks/$', 'task_list', name='task_list'),
    url(r'^tasks/(?P<pk>[0-9]+)$', 'task_detail', name='task_detail'),
    url(r'^deployment/', include('deployment.urls')),
)