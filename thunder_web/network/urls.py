from django.conf.urls import patterns, url
from network.views import *
import os.path
from django.views.generic import RedirectView

urlpatterns = patterns(
    'network.views',
    url(r'^network/', NetworkCreateView.as_view(),  name="Network"),
    url(r'^verifyNetwork/$', networkVerify,  name="Verify Network"),
    url(r'^checkConnection/$', checkNetworkConnection,  name="Chekc network connection"),
)