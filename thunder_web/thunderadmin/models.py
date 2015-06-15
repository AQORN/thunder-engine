# @author: Binoy
# @create_date: 29-April-2015
# @modified by: Binoy M V    
# @modified_date: 29-April-2015
# @linking to other page: /__init__.py
# @description:classes for the model

from django.db import models

# @author: Binoy
# @create_date: 29-April-2015
# @modified by: Binoy M V
# @modified_date: 29-April-2015
# @description: Creating the model for the pxe network
# @Parameter : models.Model
class NetworkCard(models.Model):
    name =  models.CharField(max_length = 60, default = 'eth0')
    mac_address = models.CharField(max_length = 60)
    
    class Meta:
        db_table = "install_network_card"
        
    def __unicode__(self):
        """To show the NetworkCard details
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
    
# @author: Binoy
# @create_date: 29-April-2015
# @modified by: Binoy M V
# @modified_date: 29-April-2015
# @description: Creating the model for the pxe network
# @Parameter : models.Model 
class PxeNetwork(models.Model):
    nic = models.ForeignKey(NetworkCard)
    pool_start = models.IPAddressField('Pool Start', max_length = 20)
    pool_end = models.IPAddressField('Pool End', max_length = 20)
    subnet_mask = models.IPAddressField('Subnet Mask', max_length = 20)
    gateway = models.IPAddressField('Gateway', max_length = 20)
    subnet = models.CharField('Subnet', max_length = 30, null = True, blank = True)
    ip = models.IPAddressField('IP', max_length = 30, null = True, blank = True)
    
    class Meta:
        db_table = "install_pxe_network"
        
    def __unicode__(self):
        """To show the pxe network details
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model
        """
        return self.pool_start
    
# @author: Binoy
# @create_date: 29-April-2015
# @modified by: Binoy M V
# @modified_date: 29-April-2015
# @description: Creating the model for the ThunderAccess
# @Parameter : models.Model
class ThunderAcces(models.Model):
    nic = models.ForeignKey(NetworkCard)
    ip_address = models.IPAddressField('IP Address', max_length = 20)
    subnet_mask = models.IPAddressField('Subnet Mask', max_length = 20)
    gateway = models.IPAddressField('Gateway', max_length = 20)
    dns_ip = models.IPAddressField('DNS IP', max_length = 20)
    
    class Meta:
        db_table = "install_thunder_access"
        
    def __unicode__(self):
        """To show the thunder access details
        Args:
        {
            self - request from the page
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model
        """
        return self.ip_address
    
# @author: Binoy
# @create_date: 29-April-2015
# @modified by: Binoy M V
# @modified_date: 29-April-2015
# @description: Creating the model for the InstallationStatus
# @Parameter : models.Model    
class InstallationStatus(models.Model):
    name = models.CharField('Process Name', max_length = 50)
    status = models.BooleanField('Process Status', default = False)
    progress = models.IntegerField('Process Percentage', default = 0)
    state = models.CharField('Process State', max_length = 3)
    reason = models.CharField('Process Failure Reason', max_length = 500)
    
    class Meta:
        db_table = "install_installation_status"
        
    def __unicode__(self):
        """To show the thunder access details
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