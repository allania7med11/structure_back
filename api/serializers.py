from django.contrib.auth.models import User
from rest_framework import serializers
from . import models as mds
from .models import Project
from django.db import models


def fSupportSerializer(queryset=None):
    if queryset==None:
        data={
            "Meta":type("Meta", (object,),{"model": mds.Support,"fields" : ('url', 'id','project','name', 'UX', 'UZ','RY')   }) 
        } 
    else:
        data={
            "project":serializers.HyperlinkedRelatedField(view_name='project-detail',queryset=queryset),
            "Meta":type("Meta", (object,),{"model": mds.Support,"fields" : ('url', 'id','project','name', 'UX', 'UZ','RY')   }),
        }         
    SupportSerializer=type("SupportSerializer",(serializers.HyperlinkedModelSerializer,),data) 
    return SupportSerializer
def fProjectSerializer(action=None):
    if action==None:
        data={
            "user" : serializers.ReadOnlyField(source='user.username'),
            "Meta":type("Meta", (object,),{"model": mds.Project,"fields" : ('url', 'id', 'name', 'user','auth')  }) 
        } 
    else:
        data={
            "user" : serializers.ReadOnlyField(source='user.username'),
            "supports" : fSupportSerializer()(many=True, read_only=True),
            "Meta":type("Meta", (object,),{"model": mds.Project,"fields" : ('url', 'id', 'name', 'user','auth','supports')   }),
        }         
    ProjectSerializer=type("ProjectSerializer",(serializers.HyperlinkedModelSerializer,),data) 
    return ProjectSerializer
          
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    supports = fSupportSerializer()(many=True, read_only=True)
    class Meta:
        model = mds.Project
        fields = ('url', 'id', 'name', 'user','auth','supports')

 
    
class UserSrlList(serializers.HyperlinkedModelSerializer):
    projects = serializers.HyperlinkedRelatedField(
        many=True, view_name='project-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'projects')

class UserSrlRetrieve(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')