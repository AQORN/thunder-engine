# @author: Binoy
# @create_date: 26-feb-2015
# @modified by: Binoy M V    
# @modified_date: 26-feb-2015
# @linking to other page: /__init__.py
# @description: classes for the serializer

#including the system.
from rest_framework import serializers
from task.models import Task
from cloud.models import *

# @author: Binoy
# @create_date: 26-feb-2015
# @modified by: Binoy M V    
# @modified_date: 26-feb-2015
# @description: Creating the model for the TaskSerializer
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'description', 'completed')
        
# @author: Geo Varghese
# @create_date: 03-mar-2015
# @modified by: Geo varghese    
# @modified_date: 03-mar-2015
# @description: Creating the model for the NodeSerializer
class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nodelist
        fields = ('cloud_id', 'node_ip', 'host_name')