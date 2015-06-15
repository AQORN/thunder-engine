# Add decorator functions here
# @author: Deepthy
# @create_date: 01-Apr-2015
# @modified by: Deepthy   
# @modified_date: 01-Apr-2015
# @description: Decorator function definitions

# imports
from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect, Http404

def checkFeatureAccess(request, feature):
    """
        Function to check the feature access for the 
    """

    # Set the flag
    privileged = False

    # Checks for the feature access in the role mapping set in session
    if feature in request.session['cloudAccessMapData']['featureAccess']:
        privileged = True

    return privileged

def sessionUpdate(function):
    """
        To update the session data
        Use it in views:
        @sessionUpdate
        def my_view(request):
            ....
    """

    def wrap(request, *args, **kwargs):

        # Check whether session is available.
        if request.session.has_key('cloudAccessMapData'):

            # Get the cloud and role for the user
            rbacController = RBACController()
            cloudAccessMapData = rbacController.getUserCloudAccess(request.user.id)
            cloudAccessMap = cloudAccessMapData['userCloudRoleMap'][0]
            request.session['cloudAccessMapData'] = cloudAccessMapData['userCloudRoleMap'][0]
            return function(request, *args, **kwargs)

        return wrap