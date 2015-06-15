# @author: Binoy
# @create_date: 26-feb-2015
# @modified by: Binoy M V    
# @modified_date: 26-feb-2015
# @linking to other page: /__init__.py
# @description: classes for the model

#importing the system 
from django.db import models

    
# @author: Binoy
# @create_date: 26-Feb-2015
# @modified by: Binoy M V    
# @modified_date: 26-Feb-2015
# @description: Creating the model for the task    
class Task(models.Model):
    completed = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
# Create your models here.

    def __unicode__(self):
        """To show the list with cloud name
        Args:
        {
            self - request from the page
        }
         
        Returns:
            Returns response to the html page
             
        Raises:
            Exceptions from the model                
        """
        return self.title 

    class Meta:
        db_table = "thunder_task"  