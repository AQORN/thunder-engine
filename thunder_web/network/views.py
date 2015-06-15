# Create your views here.
# @author: Binoy
# @create_date: 19-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 19-Jan-2015
# @linking to other page: /__init__.py
# @description: Functions of the users

# Including the modules
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from cloud.models import *
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.template import RequestContext
from cloud.forms import * 
from pycurl import USERNAME
from lxml.etree import tostring
from django.template import RequestContext
from requests.api import request
from django.contrib.auth.decorators import login_required
from django.db import connection
from jinja2.ext import Extension
from django.template.base import NodeList
from chardet.test import count
from django.contrib import messages
from django.conf import settings
from django.utils import decorators
from django.utils.translation import ugettext as _
from tabination.views import TabView
from logging import Handler
from django.utils import timezone
import json, datetime, random
from django.core.management.base import NoArgsCommand, CommandError
from datetime import date, timedelta, datetime
import logging
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from .forms import *
from .models import *
from network.functions import *
from time import sleep

# @author: Binoy
# @create_date: 2-March-2015
# @modified by: Binoy M V    
# @modified_date: 2-March-2015
# @description: Creating the  view
class NetworkCreateView(CreateView):
    
    # Initial form values
    template_name = 'network/network_config.html'
    model = NetworkDetails
    form_class = NetworkForm
    success_url = settings.BASE_URL+'clouds/network/saved'
    formError = {}

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        self - self values
        request - request from the page
        *args - extra variable
        **kwargs - extra variable
        """
         
        # setting the forms
        self.object = None
        publicList = []
        floatList = []
        dnsList = []
        privateList = []
         
        try:
            self.object = NetworkDetails.objects.get(cloud_id = request.session['cloudId'])

            # Getting the values from the database
            floatNetworks = FloatingNetwork.objects.filter(thunder_network_details_id = self.object.id)
            publicNetworks = PublicNetwork.objects.filter(thunder_network_details_id = self.object.id)
            dnsServers = DNSServer.objects.filter(thunder_network_details_id = self.object.id)
            privateNetworks = PrivateNetwork.objects.filter(thunder_network_details_id = self.object.id)
            
            # Setting the initial data to show in form
            for dnsServer in dnsServers:
                dnsResult = {}
                dnsResult['dns_server'] = dnsServer.dns_server
                dnsList.append(dnsResult)
            
            # Setting the initial data to show in form
            for publicNetwork in publicNetworks:
                publicResult = {}
                publicResult['ip_range_from'] = publicNetwork.ip_range_from
                publicResult['ip_range_to'] = publicNetwork.ip_range_to
                publicList.append(publicResult)
                
            # Setting the initial data to show in form
            for floatNetwork in floatNetworks:
                floatResult = {}
                floatResult['ip_range_from'] = floatNetwork.ip_range_from
                floatResult['ip_range_to'] = floatNetwork.ip_range_to
                floatResult['ip_cidr'] = floatNetwork.ip_cidr
                floatResult['use_vlan'] = floatNetwork.use_vlan
                floatResult['vlan_tag'] = floatNetwork.vlan_tag
                floatList.append(floatResult)    
            
            # Setting the initial data to show in form
            for privateNetwork in privateNetworks:
                privateResult = {}
                privateResult['network_cidr'] = privateNetwork.network_cidr
                privateList.append(privateResult)
            
            # Status details
            verifyStatus = self.object.status
            lastVerfied = self.object.last_verified
                
        except Exception, e:
            debugException(e)
            self.object = None
            verifyStatus = False
            lastVerfied = ''

        # if empty private network list add default value
        if not privateList:
            privateList.append({'network_cidr': "192.168.0.0/24"})

        # setting the forms     
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        public_network_form = PublicNetworkFormSet(initial = publicList)
        floating_network_form = FloatingNetworkFormSet(initial = floatList)
        dns_server_form = DNSserverFormSet(initial = dnsList)
        private_network_form = PrivateNetworkFormSet(initial = privateList)
                
        # returning the form 
        return self.render_to_response(
            self.get_context_data(
                form = form, verifyStatus = verifyStatus, lastVerfied = lastVerfied,
                public_network_form = public_network_form, floating_network_form = floating_network_form,
                dns_server_form = dns_server_form, private_network_form = private_network_form,
                settings = settings
            )
        )
    
    
    def commonFormValidation(self, mainForm, publicForm, floatForm, dnsForm, privateForm):
        """
        Function to validate all common checking by comparing form
        self  -  self object
        mainForm  - The main form
        publicForm - Public network form details
        floatForm - Floating IP form
        dnsForm - The dns form
        privateForm - The private network form
        @return [True/False] [valid/invalid]
        """

        checkList = []
        publicCidr = mainForm.instance.public_cidr
        mgtCidr = mainForm.instance.in_network_cidr
        stCidr = mainForm.instance.st_network_cidr
        publicVlanTag = mainForm.instance.public_vlan if mainForm.instance.public_use_vlan else False
        mgtVlanTag = mainForm.instance.in_vlan if mainForm.instance.in_use_vlan else False
        stVlanTag = mainForm.instance.st_vlan if mainForm.instance.st_use_vlan else False
        
        # check cidr values are equal
        if isCidrEqual(mgtCidr, stCidr):
            mainForm._errors['in_network_cidr'] = mainForm.error_class(["Duplicate network found"])
            checkList.append(False)
            
        # check with public network
        if publicCidr and (isCidrEqual(publicCidr, mgtCidr) or isCidrEqual(publicCidr, stCidr)):
            mainForm._errors['public_cidr'] = mainForm.error_class(["Duplicate network found"])
            checkList.append(False)
            
        # check vlan tags are dulpicate with public and management
        if publicVlanTag and (publicVlanTag == mgtVlanTag or publicVlanTag == stVlanTag):
            mainForm._errors['public_vlan'] = mainForm.error_class(["Duplicate vlan tag found"])
            checkList.append(False)
            
        # check vlan tags are dulpicate with storage network 
        if mgtVlanTag and (mgtVlanTag == stVlanTag):
            mainForm._errors['in_vlan'] = mainForm.error_class(["Duplicate vlan tag found"])
            checkList.append(False)
            
        ipRangeList = {}
        index = 0
        floatIPVlanList = {}
        
        # loop through floating IP list forms
        for form in floatForm:
            
            # if no value entered in row
            if not form.instance.ip_range_from and not form.instance.ip_range_to:
                continue;
            
            ipCidr = form.instance.ip_cidr
            vlanTag = form.instance.vlan_tag if form.instance.use_vlan else False
            networkError = False            
            
            # check whether duplicate vlans found, if cidr value equal to public cidr
            if isCidrEqual(ipCidr, publicCidr):
                
                # use same vlan tag of public network
                if vlanTag != publicVlanTag:
                    form._errors['vlan_tag'] = form.error_class(["Use same vlan tag of public network"])
                    networkError = True
                    
            else:
                
                # to get the correct IPcidr value exiting ipcidr
                realIpCidr = isValidCidr(ipCidr)  
                
                # if empty vlan tag, then tell user to use vlan tag
                if not vlanTag:
                    form._errors['vlan_tag'] = form.error_class(["Use vlan tag to add more networks"])
                    networkError = True
                elif (vlanTag == publicVlanTag) or (vlanTag == mgtVlanTag) or (vlanTag == stVlanTag):
                    
                    # chekc for dulicate vlan tags in other networks
                    form._errors['vlan_tag'] = form.error_class(["Duplicate vlan tag found"])
                    networkError = True
                    
                elif floatIPVlanList.has_key(vlanTag) and (floatIPVlanList[vlanTag] != realIpCidr):
                    
                    # check for duplicate vlan tags in different floating ip networks
                    form._errors['vlan_tag'] = form.error_class(["Duplicate vlan tag found"])
                    networkError = True
                    
                else:
                    
                    try:
                        extVlanTag = floatIPVlanList.keys()[floatIPVlanList.values().index(realIpCidr)]
                    except Exception, e:
                        extVlanTag = False
                    
                    # check whether the same network have same vlan tag 
                    if extVlanTag and extVlanTag != vlanTag:
                        form._errors['vlan_tag'] = form.error_class(["Use same vlan tag of same network"])
                        networkError = True
                    else:
                        floatIPVlanList[vlanTag] = realIpCidr
        
            # check cidr with mgt and storage
            if ipCidr and (isCidrEqual(ipCidr, mgtCidr) or isCidrEqual(ipCidr, stCidr)):
                form._errors['ip_cidr'] = form.error_class(["Duplicate network found"])
                networkError = True
            
            if networkError:
                checkList.append(False)
            else:
                
                # if no error, add to ip range
                if not ipRangeList.has_key(ipCidr):
                    ipRangeList[ipCidr] = []
                
                anchor = "F" + "-" + str(index) + "-" + form.instance.ip_range_from + "-" + form.instance.ip_range_to
                ipRangeList[ipCidr].append(anchor)
            
            index += 1
        
            
        # initialize and loop through public form
        index = 0
        for form in publicForm:
            fromIp = form.instance.ip_range_from
            toIp = form.instance.ip_range_to
            
            # if anything is present
            if fromIp or toIp:
                
                # check valid ip range added or not
                if not isValidIPRange(fromIp, toIp, publicCidr):
                    form._errors['ip_range_from'] = form.error_class(["Please enter valid ip range from network"])
                    checkList.append(False)
                else:
                    
                    # if no error add to ip range
                    if not ipRangeList.has_key(publicCidr):
                        ipRangeList[publicCidr] = []
                    
                    anchor = "P" + "-" + str(index) + "-" + fromIp + "-" + toIp
                    ipRangeList[publicCidr].append(anchor)
            
            index += 1
        
        # loop though ip range list and find any iprange overlapped
        for ipCidr, rangeList in ipRangeList.iteritems():
            
            # initialize and for each remaining list 
            netType, index, fromIp, toIp = rangeList.pop(0).split("-")
            for rangeAddr in rangeList:
                
                # initialise and verify wheteher range overlap each other
                cmpType, cmpIndex, compareFromIp, compareToIp = rangeAddr.split("-")
                if isIpRangeOverlap(fromIp, toIp, compareFromIp, compareToIp):
                    index = int(index)
                    formObj = publicForm[index] if netType == "P" else floatForm[index] 
                    formObj._errors['ip_range_from'] = form.error_class(["Ip ranges overlap each other"])
                    checkList.append(False)
        
        # if any check failed return False
        if False in checkList:
            return False
        else:
            return True
        

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        self - self values
        request - request from the page
        *args - extra variable
        **kwargs - extra variable
        """

        try:
            # setting the forms
            self.object = None
            
            # setting the form
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            public_network_form = PublicNetworkFormSet(self.request.POST)
            floating_network_form = FloatingNetworkFormSet(self.request.POST)
            dns_server_form = DNSserverFormSet(self.request.POST)
            private_network_form = PrivateNetworkFormSet(self.request.POST)
            
            # checking the validity of the form and returning the form
            if (form.is_valid()
                and public_network_form.is_valid()
                and floating_network_form.is_valid()
                and dns_server_form.is_valid()
                and private_network_form.is_valid()):
                
                # if check common validations
                if self.commonFormValidation(form, public_network_form, floating_network_form, dns_server_form, private_network_form):                
                    return self.form_valid(
                        form, public_network_form, floating_network_form, dns_server_form,
                        private_network_form, request
                    )
            
            return self.form_invalid(
                form, public_network_form, floating_network_form, 
                dns_server_form, private_network_form, request
            )

        except Exception, e:
            debugException(e)
            

    def form_valid(self, form, public_network_form, floating_network_form, dns_server_form, 
        private_network_form, request):
        """
        Called if all forms are valid. Creates a form instance along with
        associated Ingredients and Instructions and then redirects to a success page.
        self - request from the page
        form - Form data
        public_network_form - public network form
        floating_network_form  - floating network form 
        dns_server_form - dns server form  
        private_network_form - private network form
        request - request parameter
        """
       
        # deleting the values from network tables which delete data from thunder_floatingip_network, thunder_network_details, thunder_public_network, thunder_dns_server
        NetworkDetails.objects.filter(cloud_id = request.session['cloudId']).delete()
        
        # Saving the form with message
        self.object = form.save()        
        
        # save public network ranges
        public_network_form.instance = self.object
        public_network_form.instance.status = False
        public_network_form.save()
        
        # Saving the floating network form
        floating_network_form.instance = self.object
        floating_network_form.save()
        
        # Saving the dns server form
        dns_server_form.instance = self.object
        dns_server_form.save()
        
        # Adding the status and saving the private network form
        private_network_form.instance = self.object
        private_network_form.instance.status = False
        private_network_form.save()

        #setting the success message
        messages.add_message(request, messages.SUCCESS, 'Network updated successfully.')
        return HttpResponseRedirect(self.get_success_url())
    

    def form_invalid(self, form, public_network_form, floating_network_form, dns_server_form, 
        private_network_form, request):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        self - request from the page
        form - Form data
        public_network_form - public network form
        floating_network_form - floating network form  
        dns_server_form  -  dns server form
        request - request parameter
        """        

        # returning the form with error message 
        messages.add_message(request, messages.ERROR, 'Network updating failed due to error in the form values.')
        return self.render_to_response(
            self.get_context_data(
                form = form, public_network_form = public_network_form,
                floating_network_form = floating_network_form,
                dns_server_form = dns_server_form, private_network_form = private_network_form,
                form_error = self.formError, settings = settings
            )
        )


def networkVerify(request):
    return render_to_response('network/network_verify.html', {}, context_instance=RequestContext(request))


def checkNetworkConnection(request):
    '''
    function to check network connection
    request - The request parameters
    '''
    
    # Initialising and setting the data variables
    allMsgList = collections.OrderedDict()
    statusMsgList = []
    networkVerificationDetails = {}
    
    # get network details
    try:
        
        # get network details of cloud
        cloudId = request.session['cloudId']
        networkInfo = NetworkDetails.objects.get(cloud_id = cloudId)
        
        # if simulation mode is on
        if settings.SIMULATOR_MODE:
            sleep(4)
            allMsgList["Successfully tested public network"] = 1
            allMsgList["Successfully tested floating IP network"] = 1
            allMsgList["Successfully tested management network"] = 1
            allMsgList["Successfully tested storage network"] = 1
        else:
            
            # verify the public network
            [statusMsg, msgList] = verifyPublicNetwork(cloudId, networkInfo)
            allMsgList.update(msgList)
            statusMsgList.append(statusMsg)
                
            # verify the floating IP network
            [statusMsg, msgList] = verifyFloatingIpNetwork(cloudId, networkInfo)
            allMsgList.update(msgList)
            statusMsgList.append(statusMsg)
                 
            # verify the management network
            [statusMsg, msgList] = verifyManagementNetwork(cloudId, networkInfo)
            allMsgList.update(msgList)
            statusMsgList.append(statusMsg)
               
            # verify the storage network
            [statusMsg, msgList] = verifyStorageNetwork(cloudId, networkInfo)
            allMsgList.update(msgList)
            statusMsgList.append(statusMsg)
        
        # check any network verification step failed
        if "Failed" in statusMsgList:
            statusMsg = "Failed"
            networkInfo.status = 0
            networkInfo.last_verified = datetime.datetime.now()
        else:
            statusMsg = "Success"
            networkInfo.status = 1
            networkInfo.last_verified = datetime.datetime.now()
            
        # save network verification details
        networkInfo.save()

        # Set the details of verification
        networkVerificationDetails["last_verification"] = "'" + networkInfo.last_verified.strftime("%B %d, %Y, %I:%M %p") + "'"
        networkVerificationDetails["status"] = networkInfo.status
            
        # if empty message list means no networks configured
        if not allMsgList:
            statusMsg = "Failed"
            allMsgList["Networks are not configured"] = 0
         
    except NetworkDetails.DoesNotExist:
        statusMsg = "Failed"
        allMsgList["Networks are not configured"] = 0
    
    return render_to_response('network/network_check_results.html',
        {'status_msg': statusMsg, 'msgList': allMsgList, "networkVerificationDetails" : networkVerificationDetails},
        context_instance = RequestContext(request)
    )
