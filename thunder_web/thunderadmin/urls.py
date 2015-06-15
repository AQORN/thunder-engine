from django.conf.urls import patterns, url
from thunderadmin.views import *
import os.path
from django.views.generic import RedirectView

urlpatterns = patterns(
    'thunderadmin.views',
    url(r'^$', adminConfig,  name="index"),
    url(r'^config/', adminConfig,  name="adminConfig"),
    url(r'^setpxe/', setPxe,  name="setPxe"),
    url(r'^setaccess/', setAccess,  name="setAccess"),
    url(r'^inprogress/', inProgress, name = "inprogress"),
    url(r'^resetpass/', resetPassword,  name="resetPassword"),
    url(r'^resethunder/', resetThunder,  name="resetThunder"),
    url(r'^getInstallationStatus/', getInstallationStatus, name = "getInstallationStatus"),
    url(r'^installService/', installService, name = "installService"),
    url(r'^completeInstallation/', completeInstallation, name = "completeInstallation"),
    )