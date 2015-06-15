# @author: Binoy
# @create_date: 29-April-2015
# @modified by: Binoy M V    
# @modified_date: 29-April-2015
# @linking to other page: /__init__.py
# @description: Views for the admin

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from thunderadmin.models import *
from cloud.models import *
from thunderadmin.forms import * 
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from common import *
from django.contrib import messages

# Create your views here.
def pxeDetails():
    """To show the list of roles assinged
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    
    #Getting the details from the tables
    pxeNetworks = PxeNetwork.objects.all()
    
    #Setting the values for the template
    pxeList = []
    
    #Looping through the values
    for pxeNetwork in pxeNetworks:
        pxeData = {}
        pxeData['pool_start'] = pxeNetwork.pool_start
        pxeData['pool_end'] = pxeNetwork.pool_end
        pxeData['subnet_mask'] = pxeNetwork.subnet_mask
        pxeData['gateway'] = pxeNetwork.gateway
        pxeData['nic_name'] = pxeNetwork.nic.name
        pxeList.append(pxeData)

    #returning the pxe list
    return pxeList

@login_required
def adminConfig(request):
    """To show the form of pxe
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    
    # Checking whether the backend service components are installed or not.
    # If not, redirects to the installation page
    if not checkInstallationStatus():
       return installModulesScreen(request)


    #Getting the pxe form
    updated = checkAdminUpdated()

    #If the admin update not complete then showing the admin form accordingly
    if updated > 0:
        form = adminConfigForm()
    else:
        form = adminConfigForm2()
    
    #To save the form values and redirect to the clicked screen
    if request.method == 'POST' and request.POST.get('formLevel') != None:
        return HttpResponseRedirect(settings.BASE_URL + 'admin/' + request.POST.get('formLevel'))
    
    #Getting the pxe details
    pxe = pxeDetails()
    
    #Getting the data details
    data = adminSetupDetails()
    
    #returning the response to the html
    return render_to_response('thunderadmin/config.html', {'forms':form, 'datas': data}, context_instance = RequestContext(request))

def installModulesScreen(request):
    """
        Displays the module installation progress screen
    """

    try:

        # Set the initial progress value
        installationStatus = InstallationStatus.objects.filter(name = 'Installation Status')
        installationStatus = installationStatus[0]
        installationStatus.progress = 1
        installationStatus.reason = ''
        installationStatus.save()
    except Exception, e:

        print e

    # returning the response to the html
    return render_to_response('thunderadmin/progress.html', {'progress_state' : 1}, context_instance = RequestContext(request))

def getInstallationStatus(request):
    """
        Returns the initial installation status of the service modules
    """

    # Set initial data variables
    progress_state = 1
    status = False

    try:
        # Fetch the initial progress value
        installationStatus = InstallationStatus.objects.filter(name = 'Installation Status')
        installationStatus = installationStatus[0]
        progress_state = installationStatus.progress
        status = True
    except Exception, e:

        print e
        status = False

    # sending the response
    return HttpResponse(json.dumps({"status" : status, "progress_state" : progress_state}), content_type = "application/json")

def installService(request):
    """
        Function to install the service module
    """
    
    # Initialising data variables
    services = ['thunder', 'cobbler']
    installationStatus = True
    errMsg = ""
    status = True

    # Calls the function to get the node n/w card names
    nicList = getLocalNodeInformation()

    # If nics are not successfully saved, sets the error message
    if not saveNics(nicList):
        status = False
        errMsg = "Error while saving the network card details"

        # sending the response
        return HttpResponse(json.dumps({"status" : status, "progress_state" : 1, "error" : errMsg}), content_type = "application/json")

    # Loops through the service component list
    for serviceName in services:

        try:

            # Set the initial progress value
            installationStatusObj = InstallationStatus.objects.filter(name = 'Installation Status')
            installationStatusObj = installationStatusObj[0]

            # Sets the return data
            progress_state = installationStatusObj.progress

            # Executes the service installation chef command
            executionResult = executeServiceInstallation(serviceName)

            # Checks the response of the execution and set the details
            if executionResult['status'] == False:
                installationStatusObj.reason = executionResult['error']
                installationStatus = False
                installationStatusObj.state = 'F'

                # Saving the object details
                installationStatusObj.save()
                status = False
                errMsg = executionResult['error']
                break

            else:

                # Sets the progress for the installation process
                progress = installationStatusObj.progress + int(100 / 2)
                installationStatusObj.progress = 100 if progress >= 100 else progress

                # Sets the status as 1
                if installationStatusObj.progress >= 100:
                    installationStatusObj.status = 1
                    installationStatusObj.state = 'S'

                # Saving the object details
                installationStatusObj.save()

            # Sets the return data
            progress_state = installationStatusObj.progress
        except Exception, e:

            # Setting the status
            print e
            status = False

    # Calls the function to get the node n/w card names
    nicList = getLocalNodeInformation()

    # sending the response
    return HttpResponse(json.dumps({"status" : status, "progress_state" : progress_state, "error" : errMsg}), content_type = "application/json")

@login_required
def setPxe(request):
    """To show the form of pxe
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    
    #Getting the pxe form and the details
    form = PxeSetForm()
    pxe = pxeDetails()
    oldValues = None
    isSameNic = False
    
    try:

        # Getting the value from the pxe network
        if PxeNetwork.objects.filter(pk = 1).exists():
            oldValues = PxeNetwork.objects.get(pk = 1)
            form = PxeSetForm(instance = oldValues)
        
        # Setting the pxe form values and saving the form
        if request.method == 'POST':
            
            # Checks if the entry already exists
            if oldValues:
                form = PxeSetForm(request.POST or None, instance = oldValues)
            else:
                form = PxeSetForm(request.POST)

            #Checking the form is valid or not
            if form.is_valid():

                # Get thunder access set
                accessStatus = chkThunderAccessUpdated()

                # Saves the form
                form.save()

                #parameters for installation process and updating the installation
                params = {'id': 1,
                          'status': 1,
                          'state': 'S'
                          }
                setInstallStatus(params)
                
                # Fetch and set the config data from form to the template place holders
                pxeObj = PxeNetwork.objects.get(pk = 1)
                fromIp = pxeObj.pool_start
                toIp = pxeObj.pool_end
                netMask = pxeObj.subnet_mask
                gateway = pxeObj.gateway
                nicId = pxeObj.nic_id

                # Get the subnet and random ip address
                subnet = getSubnetFromNetMaskAndIP(netMask, fromIp)

                # Checks and set the pxe ip
                if accessStatus.status:
                    thunderAccessObj = ThunderAcces.objects.get(pk = 1)

                    # Checks if pxe and thunder access have same nic, then set thunder access ip as pxe ip
                    if nicId == thunderAccessObj.nic_id:
                        serverIp = thunderAccessObj.ip_address
                        isSameNic = True

                # If the pxe and thunder access have diff nics
                if not isSameNic:
                    # serverIp = getRandomIpFromSubnet(subnet[0] + "/" + subnet[1])
                    serverIp = pxeObj.pool_start

                print "serverIp : ", serverIp

                # Set the subnet and ip for pxe
                pxeObj.subnet = subnet[0] + "/" + subnet[1]
                pxeObj.ip = serverIp

                # Saves the pxe config object
                pxeObj.save()

                try:

                    # Calls the function to save the data to dhcp template settings file
                    installationDataSetUP("dhcp.template", {"subnet" : subnet[0],
                                                            "netmask" : netMask,
                                                            "router" : gateway,
                                                            "netmask" : netMask,
                                                            "from_ip" : fromIp,
                                                            "to_ip" : toIp},
                                            "/etc/cobbler/dhcp.template")
                    
                    # Calls the function to save the data to cobbler settings file
                    installationDataSetUP("cobbler_settings", {"next_server" : serverIp,
                                                               "server" : serverIp},
                                            "/etc/cobbler/settings")

                    # Calls the function to save the nfs export file
                    installationDataSetUP("nfs_exports", {"network" : subnet[0] + "/" + subnet[1]},
                                            "/etc/exports")
                    
                    # Checks whether thunder access is set
                    if accessStatus.status:

                        # Calls the function to save the data to thunder settings file
                        changeThunderIpSettings(thunderAccessObj.ip_address, serverIp)

                        return HttpResponseRedirect('../inprogress/')
#                         executionStatus = executeBackEndSetUp()
#
#                         # Checks whether the backend process worked fine
#                         if not executionStatus['status']:
#
#                             # Setting the message and redirecting to the access page
#                             messages.add_message(request, messages.ERROR, executionStatus['errMsg'])
#                             return HttpResponseRedirect('../setpxe/')
#                         else:
#
#                             # Fetch the thunder ip
#                             thunderAccessIP = ThunderAcces.objects.filter(pk = 1)
#                             return HttpResponseRedirect('http://' + thunderAccessIP.ip_address + ':' + settings.THUNDER_PORT + '/')


                except Exception, e:

                    # Setting the error message
                    print e
                    messages.add_message(request, messages.ERROR, 'Error while updating PXE Network details')
                    return HttpResponseRedirect('../setpxe/')

                #Setting the message and redirecting to the access page
                messages.add_message(request, messages.SUCCESS, 'PXE Network details updated.')
                return HttpResponseRedirect('../setaccess/')
            
    except Exception, e:

        # Setting the error message
        print e
        messages.add_message(request, messages.ERROR, 'Error while updating PXE Network details')
        return HttpResponseRedirect('../setpxe/')

    # Returning the response to the html
    return render_to_response('thunderadmin/set_pxe.html', {'forms':form, 'pxes':pxe}, context_instance = RequestContext(request))

@login_required
def setAccess(request):
    """To show the form to set the thunder access details
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    
    # Getting the Access Form and sets the data variables
    form = AccessForm()
    oldValues = None
    executionStatus = True
    
    try:

        # Getting the value from the thunder access entry and creates the form
        if ThunderAcces.objects.filter(pk = 1).exists():
            oldValues = ThunderAcces.objects.get(pk = 1)
            form = AccessForm(instance = oldValues)
        
        #Setting the Access Form values and saving the form
        if request.method == 'POST':

            # Checks if the entry already exists
            if oldValues:
                form = AccessForm(request.POST or None, instance = oldValues)
            else:
                form = AccessForm(request.POST)

            if form.is_valid():
                
                # Get the pxe update status
                pxestatus = chkPxeUpdated()
               
                # Checks the pxe update status
                if pxestatus.status:

                    # Fetch pxe config data and set to the template place holders
                    pxeObj = PxeNetwork.objects.get(pk = 1)
                    pxeNicId = int(pxeObj.nic_id)
                    thunderNicId = int(request.POST.get("nic", ""))
                    pxeSubnet = pxeObj.subnet
                    thunderIpVal = request.POST.get("ip_address", "")

                    ### Validate whether the thunder ip is in pxe subnet, if same nic is selected for both pxe and thunder access ###

                    # Check nic for pxe and thunder access and then edit the interface file
                    if pxeNicId == thunderNicId:

                        # Check whether the thunder ip given is in the subnet of the pxe nic
                        if IPAddress(str(thunderIpVal)) not in IPNetwork(str(pxeSubnet)):

                            # Set the error data
                            status = False
                            errMsg = "The thunder ip is not from the subnet provided. Please either change the nic for thunder access or provide an ip from the pxe subnet"
                            messages.add_message(request, messages.ERROR, errMsg)
                            return HttpResponseRedirect('../setaccess/')

                        else:

                            # Set the pxe ip as the thunder access ip since they are in same n/w
                            pxeObj.ip = thunderIpVal
                            pxeObj.save()

                form.save()

                # parameters for installation process and updating the installation
                params = {'id': 2,
                          'status': 1,
                          'state': 'S'
                          }
                setInstallStatus(params)

                # Checks the pxe update status
                if pxestatus.status == False:
                    return HttpResponseRedirect('../setpxe/')
                else:

                    try:

                        # Fetch and set the config data from form to the template place holders
                        thunderAccessObj = ThunderAcces.objects.get(pk = 1)
                        thunderIp = thunderAccessObj.ip_address

                        # Calls the function to save the data to thunder settings file
                        changeThunderIpSettings(thunderIp, pxeObj.ip)

                        # Calls the function to save the data to cobbler settings file
                        installationDataSetUP("cobbler_settings", {"next_server" : pxeObj.ip,
                                                                   "server" : pxeObj.ip},
                                                "/etc/cobbler/settings")

                    except Exception, e:

                        # Setting the error message
                        print e
                        messages.add_message(request, messages.ERROR, 'Error while updating thunder access details')
                        return HttpResponseRedirect('../setaccess/')

                    return HttpResponseRedirect('../inprogress/')
#                     executionStatus = executeBackEndSetUp()
#
#                     # Checks whether the backend process worked fine
#                     if not executionStatus['status']:
#
#                         # Setting the message and redirecting to the access page
#                         messages.add_message(request, messages.ERROR, executionStatus['errMsg'])
#                         return HttpResponseRedirect('../setaccess/')
#                     else:
#                         return HttpResponseRedirect('http://' + thunderIp + ':' + settings.THUNDER_PORT + '/')


                # Setting the message and redirecting to the pxe page
                messages.add_message(request, messages.SUCCESS, 'Access Updated.')

    except Exception, e:

        # Setting the error message
        print e
        messages.add_message(request, messages.ERROR, 'Error while updating thunder access details')
 
    #returning the response to the html
    return render_to_response('thunderadmin/set_access.html', {'forms':form}, context_instance = RequestContext(request))

def setInstallStatus(params):
    """To update the installation status
    Args:
        {
            params - request from the page
        }
        
    Returns:
        Returns response to the calling function
        
    Raises:
        Exceptions and redirection to the login page.
    """
    
    #To update the installation process
    InstallationStatus.objects.filter(id = params['id']).update(status = params['status'], state = params['state'])
    
@login_required
def resetPassword(request):
    """
    To update the password with the new password
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns  response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    
    #Setting the form
    form = PasswordForm()
    
    #To set the password after the post
    if request.method == 'POST':
        
        #Setting the form with the post values
        form = PasswordForm(request.POST)
        
        #Checking the form
        if form.is_valid():
            
            #updating the password
            usr = User.objects.get(pk = 1)
            usr.set_password(request.POST.get('password'))
            usr.save()
           
            #parameters for installation process and updating the installation
            params = {'id': 3,
                      'status': 1,
                      'state': 'S'
                      }
            setInstallStatus(params)
            
            #Setting the message
            messages.add_message(request, messages.SUCCESS, 'Password reset is done successfully.')

    #returning the response to the html
    return render_to_response('thunderadmin/reset_pass.html', {'forms':form}, context_instance = RequestContext(request))

@login_required
def resetThunder(request):
    """
    To update the password with the new password
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns  response to the html page
        
    Raises:
        Exceptions and redirection to the login page.
    """
    form = ResetForm()
    
    #To set the password after the post
    if request.method == 'POST':
        
        #Setting the form with the post values
        form = ResetForm(request.POST)
        
        #Checking the form
        if form.is_valid():
          
            #updating the password
            user = request.user
            
            #Checking the password to reset the thunder, if succes then reseting the thunder
            success = user.check_password(request.POST['password'])
            if success:
                #Deleting the clouds
                deleteCloudAdmin(request)
            else:
                messages.add_message(request, messages.ERROR, 'Password is wrong.')
        
    #returning the response to the html
    return render_to_response('thunderadmin/reset_thunder.html', {'forms':form}, context_instance = RequestContext(request))

def inProgress(request):
    """
        Function to display the final installation status
    """

    # returning the response to the html
    return render_to_response('thunderadmin/inprogress.html', {}, context_instance = RequestContext(request))

def completeInstallation(request):
    """
        Function to complete the final installation
    """

    # Calls the function to execute the backend setup
    executionStatus = executeBackEndSetUp()

    # Checks whether the backend process worked fine
    if executionStatus['status']:

        # Fetch and set the config data from form to the template place holders
        thunderAccessObj = ThunderAcces.objects.get(pk = 1)
        thunderIp = thunderAccessObj.ip_address
        executionStatus['url'] = 'http://' + thunderIp + ':' + settings.THUNDER_PORT + '/'

    # sending the response
    return HttpResponse(json.dumps(executionStatus), content_type = "application/json")