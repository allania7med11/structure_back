from django.contrib.auth.models import User
from rest_framework import serializers
from . import models as mds
from .models import Project
from django.db import models
from . import models as mds
from .infs import cst

def infSerializer(name):
    model= cst.models[name]
    data={
            "Meta":type("Meta", (object,),{"model": model["model"],"fields" : ('url',"name")   }) 
        }
    return type(model["name"]+"infSerializer",(serializers.HyperlinkedModelSerializer,),data)    
def fSerializer(name,user=None):
    model= cst.models[name]
    if user==None:
        data={
            "Meta":type("Meta", (object,),{"model": model["model"],"fields" : ('url', 'id','project','modified_date',*model["fields"])   }) 
        } 
        if "models" in model:
            for (k,v) in model["models"].items():
                data[k]=infSerializer(v)(read_only=True) 
    else:
        data={
            "project":serializers.HyperlinkedRelatedField(view_name='project-detail',queryset=mds.Project.objects.filter(user=user)),
            "Meta":type("Meta", (object,),{"model": model["model"],"fields" : ('url', 'id','project','modified_date',*model["fields"])   }),
        } 
        if "models" in model:
            for (k,v) in model["models"].items():  
                md=cst.models[v]
                queryset=md["model"].objects.filter(project__user=user)
                data[k]=serializers.HyperlinkedRelatedField(view_name=v[:-1]+'-detail',queryset=queryset)
                
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
            **{k:fSerializer(k)(many=True, read_only=True) for k in cst.lst},
            "nodes" : fSerializer("nodes")(many=True, read_only=True),
            "supports" : fSerializer("supports")(many=True, read_only=True),
            "bars" : fSerializer("bars")(many=True, read_only=True),
            "Meta":type("Meta", (object,),{"model": mds.Project,"fields" : ('url', 'id', 'name', 'user','auth',*cst.lst)   }),
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