# @author: Geo Varghese
# @create_date: 2-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 2-Apr-2015
# @linking to other page: 
# @description: Common download actions

# importing required modules
from cloud.common import *
from django.http import HttpResponse, Http404

def downloadFile(request, fileName):
    '''
    function to download  a file
    fileName  - The name of the file
    '''
    
    filePath = settings.THUNDER_ABS_PATH + "/download/repo/" + fileName
    f = open(filePath, 'r')
    fileData = f.read()
    f.close()
    response = HttpResponse(fileData, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' %fileName
    return response