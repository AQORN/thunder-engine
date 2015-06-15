# Create your logger here.
# @author: Binoy
# @create_date: 24-Feb-2015
# @modified by: Binoy M V    
# @modified_date: 24-Feb-2015
# @linking to other page: /__init__.py
# @description: Functions of the users

#importing the modules
import logging
import datetime

# @author: Binoy
# @create_date: 24-Feb-2015
# @modified by: Binoy M V    
# @modified_date: 24-Feb-2015
# @description: Class for the navigation base
class dbLogHandler(logging.Handler): # Inherit from logging.Handler
    def __init__(self):
        # run the regular Handler __init__
        logging.Handler.__init__(self)

    def emit(self, record):
        """To show the list with user roles
        Args:
        {
            self - request from the page
            record - record values
        }
        
        Returns:
            Returns response to the html page
            
        Raises:
            Exceptions from the model                
        """        
        # instantiate the model
        try:
            #NOTE: need to import this here otherwise it causes a circular reference and doesn't work
            #  i.e. settings imports loggers imports models imports settings...
            from thunder.models import Log
            logEntry = Log(level=record.levelname, message=record.message, timestamp=datetime.datetime.now())
            logEntry.save()
        except:
            pass

        return