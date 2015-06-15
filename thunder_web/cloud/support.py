# Create your views here.
# @author: Binoy
# @create_date: 23-Feb-2015
# @modified by: Binoy M V    
# @modified_date: 23-Feb-2015
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


@login_required
def supportTab(request):
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
     
    #setting the variable
    
    #returning the response to the html
    return render_to_response('misc/support.html', {}, context_instance=RequestContext(request))
     