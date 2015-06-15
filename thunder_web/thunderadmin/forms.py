# @author: Binoy
# @create_date: 30-April-2015
# @modified by: Binoy M V    
# @modified_date: 30-April-2015
# @linking to other page: /__init__.py
# @description: classes for the forms

#adding modules
from django import forms
from django.contrib.auth.models import User
from django.forms.forms import Form
from .models import *
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from netaddr import *
from network.functions import *
 

#Setting the choices
ADMIN_CHOICES = [
    ('setpxe', 'Configure PXE Network'),
    ('setaccess', 'Configure IP Address For THUNDER GUI'),
    ('resetpass', 'Reset Thunder Password'),
]
ADMIN_CHOICES2 = [
    ('setpxe', 'Configure PXE Network'),
    ('setaccess', 'Configure IP Address For THUNDER GUI'),
    ('resetpass', 'Reset Thunder Password'),
    ('resethunder', 'Reset Thunder')
]

# @author: Binoy
# @create_date: 30-April-2015
# @modified by: Binoy M V    
# @modified_date: 30-April-2015
# @description: Creating the model form for the PxeSetForm
class PxeSetForm(ModelForm):
    """To show the pxe form
    Args:
        {
            ModelForm - modelform
        }
        
    Returns:
        Returns html form
        
    Raises:
        Exceptions - Error on form
    """ 
    
    class Meta:
        """
            Defning the model, type of fields etc
        """
        
        #Model
        model = PxeNetwork
        
        #Fields
        fields = ['nic', 'pool_start', 'pool_end', 'subnet_mask', 'gateway']
        
        #Setting the radio select
        widgets = {'nic': forms.RadioSelect}
        
    def __init__(self, *args, **kwargs):
        super(PxeSetForm, self).__init__(*args, **kwargs)
        self.fields['nic'].empty_label = None
        self.fields['nic'].label = "Select a Network Interface Card"
        
    def clean(self):
        """
        To clean the form
        Args:
            {
                self - request to the page
            }
        Returns:
            Returns  error response
            
        Raises:
            Exceptions from the try 
        """
        
        #Getting the form details from the post
        pool_start = self.cleaned_data.get('pool_start')
        pool_end = self.cleaned_data.get('pool_end')
        subnet = self.cleaned_data.get('subnet_mask')
        try:
            
            #Checking that the pool start is greater than pool end. If so error is showing 
            if (IPAddress(pool_start) > IPAddress(pool_end)):
                self._errors["pool_start"] =  mark_safe('<ul class="errorlist"><li>Pool start should be less than Pool end.</li></ul>')
            
            #Getting the cidr
            cidrMask = getCidrFromSubnet(subnet)
            
            #Getting the start ip of the network 
            startIp = getStartIp(pool_start)
            
            #Making the new cidr value
            newCidr = str(startIp) + '/'+ str(cidrMask)
            
            #Checkign the ip range is valid with the cidr
            ipCheck = isValidIPRange(pool_start, pool_end, newCidr)
            
            #Showing error if the ip check is false
            if ipCheck == False:
                self._errors["subnet_mask"] =  mark_safe('<ul class="errorlist"><li> IP Address and Gateway should be in same network.</li></ul>')
            
            return self.cleaned_data
                
        except Exception, e:
            return self.cleaned_data
         
# @author: Binoy
# @create_date: 30-April-2015
# @modified by: Binoy M V    
# @modified_date: 30-April-2015
# @description: Creating the model form for the AccessForm
class AccessForm(ModelForm):
    """To show the AccessForm
    Args:
        {
            ModelForm - modelform
        }
        
    Returns:
        Returns html form
        
    Raises:
        Exceptions - Error on form
    """ 
    class Meta:
        """
            Defning the model, type of fields etc
        """
        
        #Model
        model = ThunderAcces
        
        #Fields
        fields = ['nic', 'ip_address', 'subnet_mask', 'gateway', 'dns_ip']
        
        #Setting the radio select
        widgets = {'nic': forms.RadioSelect}
        
    def __init__(self, *args, **kwargs):
        """
            To Set the field arguments
        """ 
        super(AccessForm, self).__init__(*args, **kwargs)
        self.fields['nic'].empty_label = None
        self.fields['nic'].label = "Select a Network Interface Card"
        
    def clean(self):
        """
        To clean the form
        Args:
            {
                self - request to the page
            }
        Returns:
            Returns  error response
            
        Raises:
            Exceptions from the try 
        """
        
        #Getting the form details from the post
        ip_address = self.cleaned_data.get('ip_address')
        subnet_mask = self.cleaned_data.get('subnet_mask')
        subnet = self.cleaned_data.get('subnet_mask')
        try:

            #Getting the cidr
            cidrMask = getCidrFromSubnet(subnet_mask)

            #Getting the start ip of the network 
            startIp = getStartIp(ip_address)

            #Making the new cidr value
            newCidr = str(startIp) + '/'+ str(cidrMask)
            
            #Making the pool end address
            pool_end = getBroadcast(newCidr)
            
            #Checking the ip range is valid with the cidr
            ipCheck = isValidIPRange(startIp, pool_end, newCidr)
            
            #Showing error if the ip check is false
            if ipCheck == False:
                self._errors["subnet_mask"] =  mark_safe('<ul class="errorlist"><li> IP Address and Gateway should be in same network.</li></ul>')
            
            return self.cleaned_data
                
        except Exception, e:
            return self.cleaned_data
# @author: Binoy
# @create_date: 30-April-2015
# @modified by: Binoy M V    
# @modified_date: 30-April-2015
# @description: Creating the form for the adminConfigForm
class adminConfigForm(forms.Form):
    """To show the adminConfigForm
    Args:
        {
            ModelForm - modelform
        }
        
    Returns:
        Returns html form
        
    Raises:
        Exceptions - Error on form
    """ 
    
    #Setting the form
    formLevel = forms.ChoiceField(widget = forms.RadioSelect(), choices = ADMIN_CHOICES, label = 'Thunder Configuration Options')
    
# @author: Binoy
# @create_date: 30-April-2015
# @modified by: Binoy M V    
# @modified_date: 30-April-2015
# @description: Creating the form for the adminConfigForm
class adminConfigForm2(forms.Form):
    """To show the adminConfigForm2
    Args:
        {
            ModelForm - modelform
        }
        
    Returns:
        Returns html form
        
    Raises:
        Exceptions - Error on form
    """ 
    #Setting the form
    formLevel = forms.ChoiceField(widget = forms.RadioSelect(), choices = ADMIN_CHOICES2, label = 'Thunder Configuration Options')
    
# @author: Binoy
# @create_date: 1-May-2015
# @modified by: Binoy M V    
# @modified_date: 1-May-2015
# @description: Creating the form  for the PasswordForm
class PasswordForm(forms.Form):
    """To show the PasswordForm
    Args:
        {
            ModelForm - modelform
        }
        
    Returns:
        Returns html form
        
    Raises:
        Exceptions - Error on form
    """
    
    #Setting the form for the password
    password = forms.CharField(widget=forms.PasswordInput, label=u'Password')
    verifyPassword = forms.CharField(widget=forms.PasswordInput, label=u'Verify Password')
    
    
    def clean(self):
        """
        To clean the form
        Args:
            {
                self - request to the page
            }
            
        Returns:
            Returns  error response
            
        Raises:
            Exceptions and redirection to the login page.
        """
        
        #Getting the password data
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('verifyPassword')
    
        #Setting the error with the password, if both password is different
        if password1 and password1 != password2:
            self._errors["password"] =  mark_safe('<ul class="errorlist"><li>Passwords don\'t match</li></ul>')
        
        #To set the password if the password not validate properly
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            self._errors["password"] =  mark_safe('<ul class="errorlist"><li>The new password must contain at least one letter and at least one digit or punctuation character.</li></ul>')
            
        #Returning the form error
        return self.cleaned_data
    
# @author: Binoy
# @create_date: 1-May-2015
# @modified by: Binoy M V    
# @modified_date: 1-May-2015
# @description: Creating the form  for the reset thunder
class ResetForm(forms.Form):
    """To show the ResetForm
    Args:
        {
            ModelForm - modelform
        }
        
    Returns:
        Returns html form
        
    Raises:
        Exceptions - Error on form
    """
    
    #Setting the form for the reset thunder
    password = forms.CharField(widget=forms.PasswordInput, label=u'Confirm Thunder Admin Password')
    
    def clean(self):
        """
        To clean the form
        Args:
            {
                self - request to the page
            }
            
        Returns:
            Returns  error response
            
        Raises:
            Exceptions and redirection to the login page.
        """
        
        #Getting the password data
        password = self.cleaned_data.get('password')
    
        #Returning the form error
        return self.cleaned_data