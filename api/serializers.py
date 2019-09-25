from django.contrib.auth.models import User
from rest_framework import serializers
from . import models as mds
from .models import Project
from django.db import models
from . import models as mds
from .infs import cst


def fSerializer(name,queryset=None):
    model= cst.models[name]
    if queryset==None:
        data={
            "Meta":type("Meta", (object,),{"model": model["model"],"fields" : ('url', 'id','project','modified_date',*model["fields"])   }) 
        } 
    else:
        data={
            "project":serializers.HyperlinkedRelatedField(view_name='project-detail',queryset=queryset),
            "Meta":type("Meta", (object,),{"model": model["model"],"fields" : ('url', 'id','project','modified_date',*model["fields"])   }),
        }         
    return type(model["name"]+"Serializer",(serializers.HyperlinkedModelSerializer,),data)
    
def fProjectSerializer(action=None):
    if action==None:
        data={
            "user" : serializers.ReadOnlyField(source='user.username'),
            "Meta":type("Meta", (object,),{"model": mds.Project,"fields" : ('url', 'id','modified_date','name', 'user','auth')  }) 
        } 
    else:
        data={
            "user" : serializers.ReadOnlyField(source='user.username'),
            "nodes" : fSerializer("nodes")(many=True, read_only=True),
            "supports" : fSerializer("supports")(many=True, read_only=True),
            "Meta":type("Meta", (object,),{"model": mds.Project,"fields" : ('url', 'id', 'name', 'user','auth',"nodes",'supports')   }),
        }         
    ProjectSerializer=type("ProjectSerializer",(serializers.HyperlinkedModelSerializer,),data) 
    return ProjectSerializer
          


 
    
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