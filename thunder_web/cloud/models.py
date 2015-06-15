# @author: Binoy
# @create_date: 19-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @linking to other page: /__init__.py
# @description:classes for the model

#adding the model
from django.db import models
from django.contrib.auth.models import User, Permission
from apt_pkg import Description
from thunder import settings
from Crypto.Random.random import choice

# status choices values
STATUSCHOICES = (
    ('N', 'New'),
    ('P', 'Pending'),
    ('S', 'Success'),
    ('F', 'Fail'), 
)

# databag category list
dataBagCatList = (
    ('user_passwords', 'User Passwords'),
    ('db_passwords', 'Database Passwords'),
    ('service_passwords', 'Service Passwords'),
    ('secrets', 'Secrets'), 
)

# openstack service list
SERVICE_LIST = (
    ('keystone', 'Keystone'),
    ('glance', 'Glance'),
    ('compute', 'Compute'),
    ('Neutron', 'Neutron'),
    ('cinder', 'Cinder'),
    ('ceph', 'Ceph'),
    ('swift', 'Swift'),
    ('dashborad', 'Dashborad'),
    ('database', 'Database Server'),
    ('messaging_server', 'Messaging Server'),
    ('common', 'Common')
)

#thunder options
optionCategoryList = (
    ('openstack_admin_details', 'OpenStack Administrator Details'),
    ('shared', 'Shared'),
    # commented enable in future
    #('storage', 'Storage'),
    #('logging', 'Logging'),
)

#option Types
optionType = (
    ('radio', 'Radio box'),
    ('checkbox', 'Check box'),
    ('textbox', 'Text box'),
    ('email', 'Email'),
)

# net type list
netTypeList = (
    ('A', 'Admin Network'),
    ('P', 'Public Network'),
    ('M', 'Management Network'),
    ('S', 'Storage Network'),
)

# @author: Binoy
# @create_date: 20-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @description: Creating the model for the cloud
class Cloud(models.Model):
    user = models.ForeignKey(User)
    cloud_name = models.CharField(max_length=255)
    created_date = models.DateField(auto_now=True)   

    class Meta:
        db_table = "thunder_cloud"  
        
    def __unicode__(self):
        """To show the list with cloud name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.cloud_name 
        
# @author: Binoy
# @create_date: 20-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @description: Creating the model for the Nodelist        
class Nodelist(models.Model):
    cloud_id = models.CharField(max_length=255,  default = 0)
    node_ip = models.GenericIPAddressField(max_length=255)
    host_name = models.CharField(max_length=255)    
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    sudo_password = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    prepared = models.BooleanField(default = False)
    preos = models.BooleanField(default = False)
    currentos = models.BooleanField(default = False)
    node_up = models.BooleanField(default = False)
    zabbix_host_id = models.IntegerField(default = 0)
    
    class Meta:
        db_table = "thunder_nodelist"
        
    def __unicode__(self):
        """To show the list with cloud name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.host_name  + " " + self.node_ip
        
# @author: Binoy
# @create_date: 20-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @description: Creating the model for the Nodelog        
class Nodelog(models.Model):
    node_listid = models.IntegerField()
    subject_id = models.IntegerField()
    log_type = models.CharField(max_length = 80, default = 'JOB')
    log_title =  models.CharField(max_length = 255)
    log_details = models.TextField()
    updated_time = models.DateTimeField(auto_now = True)
    status = models.BooleanField(default = True)

    class Meta:
        db_table = "thunder_nodelog"
      
    def __unicode__(self):
        """To show the list with log name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.log_title

# @author: Geo Varghese
# @create_date: 03-mar-2015
# @modified by: Geo Varghese
# @modified_date: 03-mar-2015
# @description: Creating the model for the job management
class Job(models.Model):   
    cloud = models.ForeignKey(Cloud)
    subject_id = models.IntegerField();
    job_type = models.CharField(max_length = 100, default = 'ROLE_ASSIGN')
    start_time = models.DateTimeField('timestamp', null = True, blank = True)
    updated_time = models.DateTimeField(auto_now = True)
    end_time = models.DateTimeField('timestamp', null = True, blank = True)
    job_status = models.CharField(max_length = 1, choices = STATUSCHOICES, default = 'N')
    job_priority = models.IntegerField(default = 1)
    job_progress = models.IntegerField(default = 0)
    visited = models.BooleanField(default = True)

    # meta class of the model class
    class Meta:
        db_table = "thunder_job" 

    def __unicode__(self):
        """To show the list 
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.job_type + " " +  self.job_status 
    
       
# @author: Binoy
# @create_date: 20-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @description: Creating the model for the Nodetype        
class Roletype(models.Model):
    role_typename = models.CharField(max_length=255)
    role_code = models.CharField(max_length=60)  
    role_details = models.TextField() 
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "thunder_roletype"        
    
    def __unicode__(self):
        """To show the list with node typename
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.role_typename     
  
# @author: Binoy
# @create_date: 10-Mar-2015
# @modified by: Binoy    
# @modified_date: 10-Mar-2015
# @description: Creating the model for the cloud specifications column        
class CloudSpecification(models.Model):
    role = models.ForeignKey(Roletype) 
    spec_category = models.CharField(max_length = 100, choices = SERVICE_LIST, default = 'common')  
    spec_name = models.CharField(max_length=200)
    spec_column = models.CharField(max_length=200)
    default_value = models.CharField(max_length=200)
    
    # model meta data details
    class Meta:
        db_table = "thunder_cloud_specification"
        
    def __unicode__(self):
        """To show the list with node  spec_column
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.spec_name   
    
  
# @author: Binoy
# @create_date: 10-Mar-2015
# @modified by: Binoy    
# @modified_date: 10-Mar-2015
# @description: Creating the model for the cloud specifications values 
class  CloudSpecValue(models.Model):
    spec = models.ForeignKey(CloudSpecification)   
    cloud = models.ForeignKey(Cloud)
    spec_value = models.CharField(max_length=200)
    
    # model meta data details
    class Meta:
        db_table = "thunder_cloud_spec_values"
        
    def __unicode__(self):
        """To show the list with node  spec_value
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.spec_value 
                       
# @author: Binoy
# @create_date: 20-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @description: Creating the model for the Recipe        
class Recipe(models.Model):
    roletype = models.ForeignKey(Roletype)
    recipe_name = models.CharField(max_length=255)    
    priority = models.IntegerField()   
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "thunder_recipe"

    def __unicode__(self):
        """To show the list with recipe name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.recipe_name 
 

# @author: Binoy
# @create_date: 27-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 27-Jan-2015
# @description: Creating the model for the Node specification        
class NodeSpec(models.Model):
    nodelist = models.ForeignKey(Nodelist)
    core = models.CharField(max_length=255)    
    ram = models.CharField(max_length=255)   
    hdd = models.CharField(max_length=255)
    mac_id = models.CharField(max_length=255)
    

    class Meta:
        db_table = "thunder_nodespec"

    def __unicode__(self):
        """To show the list with recipe name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.mac_id 
    
# @author: Binoy
# @create_date: 27-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 27-Jan-2015
# @description: Creating the model for the relation between node and the role  
class NodeRole(models.Model):
    role = models.ForeignKey(Roletype, related_name='nodeRoles', null=True)
    node = models.ForeignKey(Nodelist, related_name='nodes')
    assigned  = models.BooleanField(default=True)

    class Meta:
        db_table = "thunder_noderole"

    def __unicode__(self):
        """To show the list with recipe name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.role.role_code
    
# @author: Binoy
# @create_date: 19-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 19-Jan-2015
# @description: Creating the model for the Scope  
class Scope(models.Model):
    scope_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "thunder_scope"

    def __unicode__(self):
        """To show the list with scope name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.scope_name
    

# @author: Binoy
# @create_date: 19-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 19-Jan-2015
# @description: Creating the model for the Domain
class Domain(models.Model):
    domain_name = models.CharField(max_length=255)
    scope = models.ForeignKey(Scope, related_name='domain')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "thunder_domain"

    def __unicode__(self):
        """To show the list with domain name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.domain_name
    
## @author: Binoy
# @create_date: 19-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 19-Jan-2015
# @description: Creating the model for the Scope 
class UserRoleType(models.Model):
    role_name = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain, related_name='domainid', null=True)
    permission = models.ForeignKey(Domain, related_name='permission_id', null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "thunder_userrole_type"

    def __unicode__(self):
        """To show the list with role name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.role_name   

## @author: Binoy
# @create_date: 19-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 19-Jan-2015
# @description: Creating the model for the Permission 
class Permission(models.Model):
    permission_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "thunder_permission"

    def __unicode__(self):
        """To show the list with role name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.role_name 
    
# @author: Binoy
# @create_date: 19-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 19-Jan-2015
# @description: Creating the model for the UserRole 
class UserRole(models.Model):
    role = models.ForeignKey(UserRoleType, related_name='roleid', null=True)
    user = models.ForeignKey(User, related_name='userid', null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "thunder_userrole"

    def __unicode__(self):
        """To show the list with user roles
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.role_id

# @author: Binoy
# @create_date: 24-Feb-2015
# @modified by: Binoy M V    
# @modified_date: 24-Feb-2015
# @description: Creating the model for the log 
class Log(models.Model):
    level = models.CharField(max_length=200)
    message = models.TextField()
    timedata = models.DateTimeField('timestamp', null=True, blank=True)
    
    class Meta:
        db_table = "thunder_log"  
  
# @author: Binoy
# @create_date: 25-Feb-2015
# @modified by: Binoy M V    
# @modified_date: 25-Feb-2015
# @description: Creating the model for the addon management        
class ManageAddons(models.Model):
    addon_name = models.CharField(max_length=200)
    description = models.TextField()
    timedata = models.DateTimeField('timestamp', null=True, blank=True)
    filepath = models.FileField(upload_to='addons/')
    
    class Meta:
        db_table = "thunder_manage_addons"
        
    def __unicode__(self):
        """To show the list with name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.addon_name

# @author: Binoy
# @create_date: 11-Mar-2015
# @modified by: Binoy M V    
# @modified_date: 11-Mar-2015
# @description: Creating the model for the data bag item
class DataBagItem(models.Model):
    databag_category = models.CharField(max_length=120, choices = dataBagCatList)
    item_name =  models.CharField(max_length=200)
    item_column = models.CharField(max_length=120)
    default_value = models.CharField(max_length=200)
    
    class Meta:
        db_table = "thunder_cloud_databag_item"
        
    def __unicode__(self):
        """To show the list with item name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.item_name
    

# @author: Binoy
# @create_date: 11-Mar-2015
# @modified by: Binoy M V    
# @modified_date: 11-Mar-2015
# @description: Creating the model for the databag model
class DataBag(models.Model):
    cloud = models.ForeignKey(Cloud)
    item = models.ForeignKey(DataBagItem)
    databag_value = models.CharField(max_length=200)
    
    class Meta:
        db_table = "thunder_cloud_databag"
        
    def __unicode__(self):
        """To show the list with name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """

        return self.databag_value 
    
 
class CloudDomain(models.Model):
    """
        Model class to define domain table
    """
    
    name = models.CharField(max_length = 200)
    status = models.BooleanField(default = True)
    
    class Meta:
        db_table = "thunder_cloud_domain"
        
    def __unicode__(self):
        """To show the list with name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.name
    
 
class CloudDomainMap(models.Model):
    """
        Model class to define domain table
    """
    
    cloud = models.ForeignKey(Cloud)
    domain = models.ForeignKey(CloudDomain)
    
    class Meta:
        db_table = "thunder_cloud_domain_map"
    
class DomainRolePermission(models.Model):
    """
        Model class to define domain role permission table
    """
    
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    
    class Meta:
        db_table = "thunder_domain_role_permission"
        
    def __unicode__(self):
        """To show the list with name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.name    
    
class DomainRole(models.Model):
    """
        Model class to define domain role table
    """
    
    domain = models.ForeignKey(CloudDomain)
    permission = models.ForeignKey(DomainRolePermission)
    name = models.CharField(max_length = 200) 
    
    class Meta:
        db_table = "thunder_domain_role"
        
    def __unicode__(self):
        """To show the list with name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.name
    
class UserRoleMap(models.Model):
    """
        Model class to define domain role - user mapping
    """
    
    user = models.ForeignKey(User)
    role = models.ForeignKey(DomainRole) 
    
    class Meta:
        db_table = "thunder_user_role_mapping"
    
# @author: Binoy
# @create_date: 11-Mar-2015
# @modified by: Binoy M V    
# @modified_date: 11-Mar-2015
# @description: Creating the model for the data bag item
class ThunderOption(models.Model):
    option_category = models.CharField(max_length=120, choices = optionCategoryList)
    option_name =  models.CharField(max_length=200)
    option_column = models.CharField(max_length=120)
    default_value = models.CharField(max_length=200)
    option_type = models.CharField(max_length=120, choices = optionType)
    
    class Meta:
        db_table = "thunder_option"
        
    def __unicode__(self):
        """To show the list with item name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.option_name
    

# @author: Binoy
# @create_date: 11-Mar-2015
# @modified by: Binoy M V    
# @modified_date: 11-Mar-2015
# @description: Creating the model for the databag model
class ThunderOptionValue(models.Model):
    cloud = models.ForeignKey(Cloud)
    option = models.ForeignKey(ThunderOption)
    option_value = models.CharField(max_length=200)
    
    class Meta:
        db_table = "thunder_option_value"
        
    def __unicode__(self):
        """To show the list with name
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """
        return self.option_value


# @author: Binoy
# @create_date: 16-Apr-2015
# @modified by: Binoy M V    
# @modified_date: 16-Apr-2015
# @description: Creating the model for the alert model
class Alert(models.Model):
    alert_type =  models.CharField(max_length=60, default = 'Cloud')
    referece_id = models.IntegerField()
    alert_content = models.TextField()
    visited = models.BooleanField(default = False)
    updated_time = models.DateTimeField(auto_now = True)
    alert_status = models.CharField(max_length = 1, choices = STATUSCHOICES, default = 'N') 

    class Meta:
        db_table = "thunder_alert"
        
    def __unicode__(self):
        """
        To show the list with alert content
            self - request from the page
        """

        return self.alert_content

class PatchUpdate(models.Model):
    """
        Model class for patch updates
    """

    version = models.CharField(max_length = 120)
    type = models.CharField(max_length = 10)
    intsalled_on = models.DateTimeField(auto_now = True)
    rollbacked_on = models.DateTimeField('timestamp', null = True, blank = True)
    rollbacked_status = models.BooleanField(default = False)

    class Meta:
        """
            db table name that need to be created
        """

        db_table = "thunder_patch_updates"

    def __unicode__(self):
        """
            To display info relevant to class when called.
        """

        return self.version

class UpgradeLog(models.Model):
    """
        Model class to create the upgrade logs for thunder
    """

    version = models.CharField(max_length = 120)
    log_details = models.TextField()
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        """
            db table name that need to be created
        """

        db_table = "thunder_update_logs"

    def __unicode__(self):
        """
            To display info relevant to class when called.
        """

        return self.version
    
# @author: Geo Varghese
# @create_date: 20-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 20-Apr-2015
# @description: Creating the model for network nics
class NetworkInterface(models.Model):
    nodelist = models.ForeignKey(Nodelist)
    name =  models.CharField(max_length = 60, default = 'eth0')
    mac_address = models.CharField(max_length = 60)
    model_name = models.CharField(max_length = 120)

    # meta details
    class Meta:
        db_table = "thunder_network_interface"
        
    def __unicode__(self):
        """To show the list with alert content
        self - request from the page
        Returns response to the html page
        """
        
        return str(self.nodelist_id) + " : " + self.name 

# @author: Geo Varghese
# @create_date: 20-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 20-Apr-2015
# @description: Creating the model for network interface mapping
class NetworkInterfaceMapping(models.Model):
    nic = models.ForeignKey(NetworkInterface)
    network_type = models.CharField(max_length = 1, choices = netTypeList, default = 'A')
    ip_address = models.GenericIPAddressField(max_length = 120, null = True, blank = True)

    # meta details
    class Meta:
        db_table = "thunder_nic_mapping"
        
    def __unicode__(self):
        """
        To show the list with alert content
        self - request from the page
        """
        return str(self.nic_id) + " : " + self.network_type + " : " + str(self.ip_address)
       
        
# @author: Geo Varghese
# @create_date: 20-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 20-Apr-2015
# @description: Creating the model for node disk drives
class DiskDrive(models.Model):
    nodelist = models.ForeignKey(Nodelist)
    name =  models.CharField(max_length = 60, default = 'sda')
    system_space = models.DecimalField(max_digits = 19, decimal_places = 1)
    storage_space = models.DecimalField(max_digits = 19, decimal_places = 1)
    total_space = models.DecimalField(max_digits = 19, decimal_places = 1)
    format = models.BooleanField(default = False)

    # meta details
    class Meta:
        db_table = "thunder_disk_drive"
        
    def __unicode__(self):
        """
        To show the list with alert content
            self - request from the page
        """
        return self.name
    
# @author: Binoy
# @create_date: 25-Apr-2015
# @modified by: Binoy
# @modified_date: 25-Apr-2015
# @description: Creating the model to monitor services
class MonitorService(models.Model):
    name =  models.CharField(max_length = 200)
    command = models.CharField(max_length = 200)
    status = models.BooleanField(default=True)

    # meta details
    class Meta:
        db_table = "thunder_monitor_service"
        
    def __unicode__(self):
        """
        To show the list services that need to monitor
            self - request from the page
        """
        return self.name
    
# @author: Binoy
# @create_date: 13-June-2015
# @modified by: Binoy
# @modified_date: 13-June-2015
# @description: Creating the model to save system passwords
class SystemPassword(models.Model):
    name =  models.CharField(max_length = 200)
    value = models.CharField(max_length = 200)
    
    # meta details
    class Meta:
        db_table = "thunder_system_password"
        
    def __unicode__(self):
        """
        To show the list passwords that needed in the system
        """
        return self.name