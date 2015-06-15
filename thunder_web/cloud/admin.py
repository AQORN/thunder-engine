# @author: Binoy
# @create_date: 20-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @linking to other page: /__init__.py
# @description:classes for the model in admin area

# adding required modules
from django.contrib import admin
from .models import *

# Registering models . 

admin.site.register(Cloud)
admin.site.register(Nodelist)
admin.site.register(Nodelog)
admin.site.register(Roletype)
admin.site.register(NodeSpec)
admin.site.register(NodeRole)
admin.site.register(Scope)
admin.site.register(Domain)
admin.site.register(UserRoleType)
admin.site.register(Permission)
admin.site.register(UserRole)
admin.site.register(ManageAddons)
admin.site.register(Job)
admin.site.register(CloudSpecification)
admin.site.register(CloudSpecValue)
admin.site.register(DataBag)
admin.site.register(DataBagItem)
admin.site.register(ThunderOption)
admin.site.register(ThunderOptionValue)
admin.site.register(DomainRolePermission)
admin.site.register(Recipe)
admin.site.register(CloudDomain)
admin.site.register(Alert)
admin.site.register(NetworkInterface)
admin.site.register(NetworkInterfaceMapping)
admin.site.register(DiskDrive)
admin.site.register(MonitorService)
admin.site.register(PatchUpdate)
admin.site.register(SystemPassword)

## @author: Binoy
# @create_date: 24-Feb-2015
# @modified by: Binoy M V    
# @modified_date: 24-Feb-2015
# @description: Creating the class for the system error 
class SystemErrorLogAdmin(admin.ModelAdmin):
    
    ordering = ('-timedata',)
    list_display = ('level', 'message', 'timedata',)
    list_filter = ('level',)
    search_fields = ('level','message',)

#     def has_add_permission(self, request):
#         return False
# 
#     def get_readonly_fields(self, request, obj=None):
#         return self.readonly_fields + ('level', 'message', 'timestamp')
admin.site.register(Log, SystemErrorLogAdmin)