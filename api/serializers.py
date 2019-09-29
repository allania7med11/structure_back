from django.contrib.auth.models import User
from rest_framework import serializers
from . import models as mds
from .models import Project
from django.db import models    
from . import models as mds
from .infs import cst

def applySerializer(name):
    model= cst.models[name]
    def save(self):
        print(self.validated_data)
        print({"pk":self.context["pk"]})
        instance=model["model"].objects.get(id=self.context["pk"])
        apply = model["apply"]
        modelApply= cst.models[apply]
        action= self.validated_data.pop('action')
        lst= self.validated_data.pop('lst')
        project = instance.project
        if action == 'apply':
            if lst == "*":
                qr = modelApply["model"].objects.filter(project=project)
                print(qr)
            else:
                L = cst.rlist(lst)
                qr = modelApply["model"].objects.filter(
                    project=project, name__in=L)
        elif action == 'remove':
            if lst == "*":
                qr = getattr(instance,apply).filter(project=project)
            else:
                L = cst.rlist(lst)
                qr = getattr(instance,apply).filter(
                    project=project, name__in=L)               
        if instance and qr:
            print("qr")
            print(qr)
            print(instance)
            print(lst)
            if action == "apply":
                getattr(instance, apply).add(*qr)
                print({'apply':getattr(instance, apply).all()})
                print(lst)
            elif action == 'remove':
                if "default" in model:
                    model_default = cst.get_default(name)
                    getattr(model_default, apply).add(*qr)
                else:
                    getattr(instance, apply).remove(*qr)    
        return instance
    data={ 
            "lst" : serializers.CharField(label="List of "+model['apply']),
            "action" : serializers.ChoiceField(default="apply",choices=[("apply", "apply"),('remove', 'remove'),]),
            "save":save,
        }
    return type(model["name"]+"applySerializer",(serializers.Serializer,),data)
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
     
    if "apply" in model:
        data[model["apply"]]=infSerializer(model["apply"])(many=True,read_only=True)            
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
          


 
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    projects = serializers.HyperlinkedRelatedField(
        many=True, view_name='project-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'projects')

