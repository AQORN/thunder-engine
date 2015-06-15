# @author: Binoy
# @create_date: 29-April-2015
# @modified by: Binoy M V    
# @modified_date: 29-April-2015
# @linking to other page: /__init__.py
# @description: admin area registration

from django.contrib import admin
from .models import *

# Registering models here.
admin.site.register(NetworkCard)
admin.site.register(PxeNetwork)
admin.site.register(ThunderAcces)
admin.site.register(InstallationStatus)