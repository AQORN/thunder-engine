# @author: Binoy
# @create_date: 21-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 21-Jan-2015
# @linking to other page: /__init__.py
# @description: Functions for the jinja template tags

from django_jinja import library
from django import template 
from django.forms import CheckboxInput
import re 
from django.core.urlresolvers import reverse
 
register = template.Library()

@library.global_function
def upper_case(name):
    """To make the name upper case
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
    
    #returning the upper case		
    return name.upper()


@library.filter
def lower_case(name):
    """To make the name lower case
    Args:
        {
            request - request from the page
        }
        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """

    #making name lower
    return name.lower()


# @author: Binoy
# @create_date: 16-Mar-2015
# @modified by: Binoy M V    
# @modified_date: 16-Mar-2015
# @description: class to set the variable 
class SetVarNode(template.Node):
 
    def __init__(self, varName, varValue):
        self.varName = varName
        self.varValue = varValue
 
    def render(self, context):
        """To make the name lower case
        Args:
            {
                self - request from the page 
                context - token
            }        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.                
        """
        try:
            value = template.Variable(self.varValue).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.varName] = value
        return u""
 
def set_var(parser, token):
    """To make the name lower case
    Args:
        {
            parser - request from the page to parse
            token - token
        }        
    Returns:
        Returns response to the html page
        
    Raises:
        Exceptions and redirection to the login page.                
    """
    """
        {% set <varName>  = <varValue> %}
    """
    
    #getting the contents
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <varName>  = <varValue> %}")
    
    #returning the values
    return SetVarNode(parts[1], parts[3])
 
register.tag('set', set_var)


@register.filter(name='is_checkbox')
def is_checkbox(field):
    """To check the field is checkbox or not
    Args:
        {
            field - request from the page which should be a field            
        }        
    Returns:
        Returns response to the html template
    """
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__  

@register.filter(name='replace')
def replace(string, args):
    """To replace the string with another one
    Args:
        {    
            string - string to find and replace
            args   - arguments         
        }        
    Returns:
        Returns response to the html template
    """
    
    #getting the search and replace string
    search  = args.split(args[0])[1]
    replace = args.split(args[0])[2]
    
    #Returning the string
    return re.sub( search, replace, string ) 

#@register.filter(name='navactive')
#  def navactive(request, urls):
#      """To replace the string with another one
#      Args:
#          {    
#              request - request from the url
#              urls - url parameter from the menu page 
#          }        
#      Returns:
#          Returns response to the html template as null or sidebar-panel-selected
#      """
#      
#      #Checking the url and request path and returning the class data
#      if urls in request.path:
#          return "sidebar-panel-selected"
#      return ""