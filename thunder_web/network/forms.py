# @author: Binoy
# @create_date: 20-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @linking to other page: /__init__.py
# @description: classes for the forms

from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from network.models import *
from network.functions import *
from django.conf import settings
from django.forms.models import BaseInlineFormSet


# @author: Binoy
# @create_date: 2-March-2015
# @modified by: Binoy M V    
# @modified_date: 2-March-2015
# @description: Creating the form  
class NetworkForm(ModelForm):
    class Meta:
        model = NetworkDetails

    def clean(self):
        """
        Validating function for customisations
        self -  self object
        """

        # Get the data of vlans
        cleaned_data = super(NetworkForm, self).clean()
        publicVlanCheck = cleaned_data.get("public_use_vlan")
        publicVlanValue = cleaned_data.get("public_vlan")
        managementVlanCheck = cleaned_data.get("in_use_vlan")
        managementVlanValue = cleaned_data.get("in_vlan")
        storageVlanCheck = cleaned_data.get("st_use_vlan")
        storageVlanValue = cleaned_data.get("st_vlan")
        publicCidr = cleaned_data.get("public_cidr")
        mgtCidr = cleaned_data.get("in_network_cidr")
        stCidr = cleaned_data.get("st_network_cidr")

        # Check for public n/w Vlan
        if publicVlanCheck and publicVlanValue is None:
            self._errors['public_vlan'] = self.error_class(["Please enter a value"])

        # Check for Management n/w Vlan
        if managementVlanCheck and managementVlanValue is None:
            self._errors['in_vlan'] = self.error_class(["Please enter a value"])

        # Check for storage n/w Vlan
        if storageVlanCheck and storageVlanValue is None:
            self._errors['st_vlan'] = self.error_class(["Please enter a value"])
            
        # check cidr values are valid
        if not isValidCidr(mgtCidr):
            self._errors['in_network_cidr'] = self.error_class(["Please enter valid CIDR"])

        # check cidr values are valid
        if stCidr and not isValidCidr(stCidr):
            self._errors['st_network_cidr'] = self.error_class(["Please enter valid CIDR"])

        # check cidr values are valid
        if publicCidr and not isValidCidr(publicCidr):
            self._errors['public_cidr'] = self.error_class(["Please enter valid CIDR"])

        # Always return the cleaned data
        return cleaned_data


# @author: geo
# @create_date: 15-May-2015
# @modified by: geo    
# @modified_date: 15-May-2015
# @description: Creating the form  
class CustomFloatFormSet(BaseInlineFormSet):
    
    def clean(self):
        """
        Validating function
        self - self object
        """
        
        super(CustomFloatFormSet, self).clean()
        
        # loop through forms
        for form in self.forms:
            fromIp = form.instance.ip_range_from
            toIp = form.instance.ip_range_to
            ipCidr = form.instance.ip_cidr
            
            # if anything is present
            if fromIp or toIp:
                
                # chekc valid ip range added or not
                if not isValidIPRange(fromIp, toIp, ipCidr):
                    form._errors['ip_range_from'] = self.error_class(["Please enter valid ip range from network"])
                    
            # if vlan chekc box enabled and vlan tag empty
            if form.instance.use_vlan and not form.instance.vlan_tag:
                form._errors['vlan_tag'] = self.error_class(["Please enter vlan tag"])


# @author: geo
# @create_date: 15-May-2015
# @modified by: geo    
# @modified_date: 15-May-2015
# @description: Creating the form  
class CustomPrivateFormSet(BaseInlineFormSet):
    
    def clean(self):
        """
        Validating function
        self - self object
        """
        
        super(CustomPrivateFormSet, self).clean()
        privateNetList = []
        
        # loop through forms
        for form in self.forms:
            privateNetList.append(form.instance.network_cidr) if form.instance.network_cidr else False
            ipCidr = form.instance.network_cidr 
                 
            # chekc valid ip range added or not
            if ipCidr and not isValidCidr(ipCidr):
                form._errors['network_cidr'] = self.error_class(["Please enter valid network"])
        
        # if no private network found
        if not privateNetList:
            self.forms[0]._errors['network_cidr'] = self.error_class(["Please enter valid network"])
        
        # initialize index and loop through private list
        index = 0
        while privateNetList:
            
            # initialise and loop through remaining list
            checkCidr = privateNetList.pop(0)
            for cidr in privateNetList:
                
                # if cidrs equal show error
                if isCidrEqual(checkCidr, cidr):
                    self.forms[index]._errors['network_cidr'] = self.error_class(["Duplicate networks found"])
            
            index += 1


# @author: geo
# @create_date: 17-May-2015
# @modified by: geo    
# @modified_date: 17-May-2015
# @description: Creating the form  
class CustomDnsFormSet(BaseInlineFormSet):
    
    def clean(self):
        """
        Validating function
        self - self object
        """
        
        super(CustomDnsFormSet, self).clean()
        dnsList = []
        
        # loop through forms
        for form in self.forms:
            dnsList.append(form.instance.dns_server) if form.instance.dns_server else False
            
        if len(set([x for x in dnsList if dnsList.count(x) > 1])) > 0:
            self.forms[0]._errors['dns_server'] = form.error_class(["Duplicate ip found"])


# adding the options to the forms to hide extra fields
PublicNetworkFormSet = inlineformset_factory(
    NetworkDetails, PublicNetwork, extra = settings.NETWORK_EXTRA_FIELD,
    can_delete = False
)

FloatingNetworkFormSet = inlineformset_factory(
    NetworkDetails, FloatingNetwork, extra = settings.NETWORK_EXTRA_FIELD,
    can_delete = False, formset = CustomFloatFormSet
)

DNSserverFormSet = inlineformset_factory(
    NetworkDetails, DNSServer, extra = settings.NETWORK_EXTRA_FIELD,
    can_delete = False, formset = CustomDnsFormSet
)

PrivateNetworkFormSet = inlineformset_factory(
    NetworkDetails, PrivateNetwork, extra = settings.NETWORK_EXTRA_FIELD,
    can_delete = False, formset = CustomPrivateFormSet
)
