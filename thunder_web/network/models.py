# @author: Binoy
# @create_date: 26-feb-2015
# @modified by: Binoy M V    
# @modified_date: 26-feb-2015
# @linking to other page: /__init__.py
# @description: classes for the model

# including the model    
from django.db import models
from cloud.models import *

# @author: Binoy
# @create_date: 2-March-2015
# @modified by: Binoy M V    
# @modified_date: 2-March-2015
# @description: Creating the model for the cloud  
# @Parameter : Label, length 
class NetworkDetails(models.Model):
    cloud = models.ForeignKey(Cloud)
    public_cidr = models.CharField('CIDR', max_length = 20, blank = True, null = True)
    public_use_vlan = models.BooleanField('Use VLAN', default = False)
    public_vlan = models.IntegerField(max_length = 4, blank = True, null = True)
    in_network_cidr = models.CharField('CIDR', max_length = 20)
    in_use_vlan = models.BooleanField('Use VLAN', default = False)
    in_vlan = models.IntegerField(max_length = 4, blank = True, null = True)
    st_network_cidr = models.CharField('CIDR', max_length = 20, blank = True, null = True)
    st_use_vlan = models.BooleanField('Use VLAN', default = False)
    st_vlan = models.IntegerField(max_length = 4, blank = True, null = True)
    gre_tunnel_from = models.IntegerField('GRE Tunnel Range', max_length = 5, default = 1)
    gre_tunnel_to = models.IntegerField(max_length = 5, default = 1000)
    update_date = models.DateTimeField('timestamp', null = True, blank = True)
    last_verified = models.DateTimeField('timestamp', null = True, blank = True)
    status = models.BooleanField(default = False)
    
    class Meta:
        db_table = "thunder_network_details"
        
    def __unicode__(self):
        """
        To show the list with cloud name
        self - request from the page                
        """
        return self.public_cidr

    
# @author: Binoy
# @create_date: 2-March-2015
# @modified by: Binoy M V    
# @modified_date: 2-March-2015
# @description: Creating the model for the cloud    
# @Parameter : Label, length
class  FloatingNetwork(models.Model):
    thunder_network_details = models.ForeignKey(NetworkDetails)
    ip_range_from = models.IPAddressField('IP Range', max_length = 20)
    ip_range_to = models.IPAddressField(max_length = 20)
    ip_cidr = models.CharField('CIDR', max_length = 20)
    use_vlan = models.BooleanField('Use VLAN', default = False)
    vlan_tag = models.IntegerField(max_length = 4, blank = True, null = True)
    
    class Meta:
        db_table = "thunder_floatingip_network"  
        
    def __unicode__(self):
        """
        To show the list with cloud name
        self - request from the page                
        """
        
        return self.ip_range_from
    
    
# @author: Binoy
# @create_date: 2-March-2015
# @modified by: Binoy M V    
# @modified_date: 2-March-2015
# @description: Creating the model for the cloud   
# @Parameter : Label, length 
class PublicNetwork(models.Model):
    thunder_network_details = models.ForeignKey(NetworkDetails)
    ip_range_from = models.IPAddressField('IP Range', max_length = 20)
    ip_range_to = models.IPAddressField(max_length = 20)
    
    class Meta:
        db_table = "thunder_public_network"  
        
    def __unicode__(self):
        """
        To show the list with cloud name
        self - request from the page                
        """
        return self.ip_range_from

   
# @author: Binoy
# @create_date: 2-March-2015
# @modified by: Binoy M V    
# @modified_date: 2-March-2015
# @description: Creating the model for the cloud    
# @Parameter : Label, length
class DNSServer(models.Model):
    thunder_network_details = models.ForeignKey(NetworkDetails)
    dns_server = models.IPAddressField('DNS Server', max_length=20)
    
    class Meta:
        db_table = "thunder_dns_server"  
        
    def __unicode__(self):
        """
        To show the list with cloud name
        self - request from the page                
        """
        return self.dns_server
    

class PrivateNetwork(models.Model):
    """
    Class to define the private network cidr
    """

    thunder_network_details = models.ForeignKey(NetworkDetails)
    network_cidr = models.CharField('Private Guest Network (CIDR)', max_length = 20)

    class Meta:
        db_table = "thunder_private_network"

    def __unicode__(self):
        """
        To show the private CIDR
        """

        return self.network_cidr
    