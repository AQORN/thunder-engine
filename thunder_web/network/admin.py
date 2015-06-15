# @author: Binoy
# @create_date: 2-March-2015
# @modified by: Binoy M V    
# @modified_date: 2-March-2015
# @linking to other page: /__init__.py
# @description: model registration in admin side

from django.contrib import admin
from .models import *
admin.site.register(NetworkDetails)
admin.site.register(FloatingNetwork)
admin.site.register(PublicNetwork)
admin.site.register(DNSServer)