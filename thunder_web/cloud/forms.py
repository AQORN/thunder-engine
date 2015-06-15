# @author: Binoy
# @create_date: 20-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @linking to other page: /__init__.py
# @description: classes for the forms

#adding modules
from django import forms
from django.core.validators import re
from django.contrib.auth.models import User
from django.forms.forms import Form
from .models import *
from logging import PlaceHolder
from _mysql import NULL
from django.forms.formsets import formset_factory

# @author: Binoy
# @create_date: 20-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 20-Jan-2015
# @description: Creating the model for the Project
class RegistrationForm(forms.Form):
    username = forms.CharField(label=u'Username', max_length=30)
    email = forms.EmailField(label=u'E-mail address')
    password1 = forms.CharField(label=u'Password',
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=u'Password (again)',
                                widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        """To clean the username
        Args:
            {
                self - request from the page          
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.                
        """
        
        #checking the username is a valid one
        if not re.search(r'^\w+$', self.cleaned_data['username']):
            raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
        
        #try catch to get the users
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        
        #raising the error if user already available
        raise forms.ValidationError(u'This username is already taken. Please choose another.')

    def clean(self):
        """To clean and validate the inputs
        Args:
            {
                self - request from the page          
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.                
        """
        
        #checking the password 1 and 2, raising the error if the password is not matching 
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'You must type the same password each time.')
        return self.cleaned_data

    def save(self):
        """To show the main page
        Args:
            {
                self - request from the page          
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.                
        """
        
        #creating the new user
        new_user = User.objects.create_user(username=self.cleaned_data['username'], 
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
        return new_user
    

# @author: Binoy
# @create_date: 21-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 21-Jan-2015
# @description: Creating the model for the Project Form
class CloudForm(forms.Form):
    """To show the main page
        Args:
            {
                self - request from the page          
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.                
    """  
    cloud_name = forms.CharField(label=u'Project Name', max_length=30) 
    
    #Meta class 
    class Meta:
        
        #model
        model = Cloud
        
        #setting the fields
        fields = ('cloud_name','user_id')    
    
    def clean_cloud_name(self):
        """To show the main page
        Args:
            {
                self - request from the page          
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.                
        """
        
        #Checking the form value, it will accept only apha neumeric values.
        if not re.match(r'^[a-zA-Z0-9 ]{2,30}$', self.cleaned_data['cloud_name']):
            raise forms.ValidationError("Only Alpha numeric values will be accepted.")
        
        #Checking the validity of the cloud name 
        if self.cleaned_data['cloud_name'].strip() == "":
            raise forms.ValidationError("Please give valid name.")
        
        # Checks whether the cloud name already exists or not
        if Cloud.objects.filter(cloud_name = self.cleaned_data['cloud_name']).exists():
            raise forms.ValidationError(u'Cloud name "%s" is already in use.' % self.cleaned_data['cloud_name'])

        return self.cleaned_data['cloud_name']

# @author: Binoy
# @create_date: 21-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 21-Jan-2015
# @description: Creating the model for the Project Form
class RecipeForm(forms.Form):
    """To show the main page
        Args:
            {
                self - request from the page          
            }
             
        Returns:
            Returns response to the html page
             
        Raises:
            Exceptions and redirection to the login page.                
    """    
      
    #Shows the cloud and recipe forms 
    Cloud = forms.ModelChoiceField(Cloud.objects, widget=forms.Select)
    recipe = forms.ModelChoiceField(Recipe.objects, widget=forms.Select(attrs={'disabled': 'false'}))
     
    #meta class to show the model
    class Meta:
        model = Cloud

# @author: Binoy
# @create_date: 29-Jan-2015
# @modified by: Binoy M V    
# @modified_date: 29-Jan-2015
# @description: Creating the form for the search form, added the widget into the form to support the place holder        
class SearchRoleForm(forms.Form):
    query = forms.CharField(label = 'search...', max_length = 30, widget = forms.TextInput(attrs = {'placeholder': 'Search...'}))  

# @author: Binoy
# @create_date: 11-Mar-2015
# @modified by: Binoy M V    
# @modified_date: 11-Mar-2015
# @description: Creating the form for the cloud configuration        
class cloudConfigForm(forms.Form):
     
    def __init__(self, *args, **kwargs):   
        super(cloudConfigForm, self).__init__(*args, **kwargs)  
        global cloud_specs
        cloud_specs = CloudSpecification.objects.all().order_by('spec_category')

        #To add the form fields , help text for the grouping         
        for cloud_spec in cloud_specs:
            self.fields[cloud_spec.spec_column] = forms.CharField(label = cloud_spec.spec_name, help_text = cloud_spec.spec_category, widget = forms.TextInput(attrs = {'placeholder': cloud_spec.default_value}))
    
    def clean(self):
        """To show the error messge if the values are not valid one
        Args:
            {
                self - request from the page
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.                
        """
        
        #Looping through the list and doing the validation
        for cloud_spec in cloud_specs:
            
            column = cloud_spec.spec_column
            try:
                print self.cleaned_data[column]
                if not re.match(r'^[0-9a-zA-Z!@#$%^&*()]*$', self.cleaned_data[column]):
                    from django.forms.util import ErrorList
                    self._errors[column] = ErrorList()
                    self._errors[column].append('Special Characters won\'t allow.')
            except Exception, e:
                self._errors[column].append('')
                
     
# @author: Binoy
# @create_date: 11-Mar-2015
# @modified by: Binoy M V    
# @modified_date: 11-Mar-2015
# @description: Creating the form for the databag configuration        
class dataBagConfigForm(forms.Form):
   
    def __init__(self, *args, **kwargs):   
        super(dataBagConfigForm, self).__init__(*args, **kwargs) 
        global databag_items
        databag_items = DataBagItem.objects.all().order_by('databag_category')
 
        #To add the form fields, help text for the grouping
        for databag_item in databag_items:
            self.fields[databag_item.item_column] = forms.CharField(label = databag_item.item_name, help_text = databag_item.databag_category, widget = forms.TextInput(attrs = {'value': databag_item.default_value}))

    def clean(self):
        """To show the error messge if the values are not valid one
        Args:
            {
                self - request from the page
            }
            
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions and redirection to the login page.                
        """
        for databag_item in databag_items:
            column = databag_item.item_column
            try:
                print self.cleaned_data[column]
                if not re.match(r'^[0-9a-zA-Z!@#$%^&*()]*$', self.cleaned_data[column]):
                    from django.forms.util import ErrorList
                    self._errors[column] = ErrorList()
                    self._errors[column].append('Special Characters won\'t allow.')
            except Exception, e:
                self._errors[column].append('')
               
# @author: Binoy
# @create_date: 24-Mar-2015
# @modified by: Binoy M V    
# @modified_date: 24-Mar-2015
# @description: Creating the form for the option configuration
class optionsForm(forms.Form):
   
    def __init__(self, *args, **kwargs):   
        super(optionsForm, self).__init__(*args, **kwargs) 
        optionItems = ThunderOption.objects.all().order_by('option_category')
        
        #Radio choices
        RADIO_CHOICES = (
            ('udp', "UDP"),
            ('tcp', "TCP"),
        )
            
        #To add the form fields, help text for the grouping
        for optionItem in optionItems:
            
            #check box values
            CHECKBOX_CHOICE = (('1', '0'),)
            
            #checking the option type
            if optionItem.option_type == 'radio':
                self.fields[optionItem.option_column] = forms.ChoiceField(label = optionItem.option_name, help_text = optionItem.option_category, widget=forms.RadioSelect, choices = RADIO_CHOICES)
            elif optionItem.option_type == 'checkbox': 
                self.fields[optionItem.option_column] = forms.ChoiceField(widget=forms.CheckboxInput, choices = CHECKBOX_CHOICE, label = optionItem.option_name, help_text = optionItem.option_category)
            elif optionItem.option_type == 'email': 
                self.fields[optionItem.option_column] = forms.CharField(widget=forms.EmailInput, label = optionItem.option_name, help_text = optionItem.option_category)
            else:
                self.fields[optionItem.option_column] = forms.CharField(label = optionItem.option_name, help_text = optionItem.option_category, widget = forms.TextInput(attrs = {'placeholder': optionItem.default_value}))
                
# @author: Binoy
# @create_date: 22-Apr-2015
# @modified by: Binoy M V    
# @modified_date: 22-Apr-2015
# @description: Creating the model for the Disk drives
class DiskDriveForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput())
    system_space = forms.CharField( help_text = 'SDA', max_length = 30, required = True, label = 'SYSTEM')
    storage_space = forms.CharField(max_length = 30, required = True, label = 'DATA')
    total_space = forms.CharField(widget=forms.HiddenInput())
    diskId = forms.CharField(widget=forms.HiddenInput())
    
    def clean(self):
        """For the validation of the form data
        Args:
            {
                self - request from the page
            }
            
        Returns:
            Returns - cleaned data
            
        Raises:
            Exceptions - Error from the form.
        """
        
        #Getting the values from the form
        cleaned_data = super(DiskDriveForm, self).clean()
        systemCheck = cleaned_data.get("system_space")
        storageCheck = cleaned_data.get("storage_space")
        totalCheck = cleaned_data.get("total_space")
        
        #If the system is error, then error message need to show 
        if systemCheck is None:
            self._errors['system_space'] = self.error_class(["Please enter a system value"])
        
        #If the Storage is error, then error message need to show 
        if storageCheck is None:
            self._errors['storage_space'] = self.error_class(["Please enter a storage value"])
            
        # Always return the cleaned data
        return cleaned_data
    
    def save(self):
        """ To save the data into the database """
        cleaned_data = super(DiskDriveForm, self).clean()
        
        #Saving the data and returning the value
        try:
            saved = DiskDrive.objects.filter(id = cleaned_data.get("diskId")).update(system_space = cleaned_data.get("system_space"), storage_space = cleaned_data.get("storage_space"))
            return saved
        except Exception,e:
            return cleaned_data      