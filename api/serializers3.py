from django.contrib.auth.models import User
from rest_framework import serializers
from . import models as mds
from .models import Project
from django.db import models    
from . import models as mds
from .infs import cst
class CSerializer:
    def __init__(self, name):
        self.name = name
    @property    
    def model(self):
        return cst.models[self.name]
    @property    
    def apply(self): 
        return self.model.get("apply")
    @property
    def modelApply(self): 
        return cst.models[self.apply]
    @property
    def saveApply(self):
        def fct(slf):
            print(slf.validated_data)
            print({"pk":slf.context["pk"]})
            instance=self.model["model"].objects.get(id=slf.context["pk"])
            action= slf.validated_data.pop('action')
            lst= slf.validated_data.pop('lst')
            project = slf.validated_data.pop('project')
            if action == 'apply':
                if lst == "*":
                    qr = self.modelApply["model"].objects.filter(project=project)
                    print(qr)
                else:
                    L = cst.rlist(lst)
                    qr = self.modelApply["model"].objects.filter(
                        project=project, name__in=L)
            elif action == 'remove':
                if lst == "*":
                    qr = getattr(instance,self.apply).filter(project=project)
                else:
                    L = cst.rlist(lst)
                    qr = getattr(instance,self.apply).filter(
                        project=project, name__in=L)               
            if instance and qr:
                if action == "apply":
                    getattr(instance, self.apply).add(*qr)
                elif action == 'remove':
                    if "default" in self.model:
                        model_default = cst.get_default(self.name)
                        getattr(model_default, self.apply).add(*qr)
                    else:
                        getattr(instance, self.apply).remove(*qr)    
            return instance
        return fct
    @property
    def get_project(self):
        def fct(slf, instance):
            request=slf.context["request"]
            print({"user":request.user})
            qs = mds.Project.objects.filter(user=request.user)
            serializer=serializers.ModelSerializer(queryset=qs)
            return serializer.data  
        return fct
    @property    
    def get_apply(self):
        def fct(slf, instance):
            request=slf.context["request"]
            print({"user":request.user})
            qs = self.modelApply["model"].objects.filter(**{"project__user":request.user,self.model["name"]:instance})
            serializer=serializers.ModelSerializer(queryset=qs,many=True,read_only=True)
            return serializer.data  
        return fct
    def get_(self,md):
        def fct(slf, instance):
            request=slf.context["request"]
            print({"user":request.user})
            qs = md["model"].objects.filter(project__user=request.user)
            serializer=serializers.ModelSerializer(queryset=qs,many=True,read_only=True)
            return serializer.data   
        return fct
    
    def fSerializer(self):
        data={
                "project":serializers.SerializerMethodField('get_project'),
                'get_project':self.get_project,
                "Meta":type("Meta", (object,),{"model": self.model["model"],"fields" : ('url', 'id','project','modified_date',*self.model["fields"])   }),
            }
        if "models" in self.model:
            for (k,v) in self.model["models"].items():  
                md=cst.models[v]
                data[k]=serializers.SerializerMethodField('get_'+k)
                data["get_"+k]=self.get_(md)
        if "apply" in self.model:
            data[self.apply]=serializers.SerializerMethodField('get_'+self.apply)
            data["get_"+self.apply]=self.get_apply           
        return type(self.model["name"]+"Serializer",(serializers.ModelSerializer,),data)
    @property
    def applySerializer(self):
        data={ 
            "project":serializers.SerializerMethodField('get_project'),
            'get_project':self.get_project,
            "lst" : serializers.CharField(label="List of "+self.apply),
            "action" : serializers.ChoiceField(default="apply",choices=[("apply", "apply"),('remove', 'remove'),]),
            "save":self.saveApply,
        }
        return type(self.model["name"]+"applySerializer",(serializers.Serializer,),data)
