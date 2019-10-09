from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import models    
from api.infs import cst
from api.help.serializers import UserRelatedField,ProjectRelatedField
from api import models as mds  
from api.help.RDM import CG
import json
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
    def saveSection(self):
        def create(slf, validated_data):
            validated_data["features"]=json.loads(validated_data["features"])
            validated_data.update(CG(validated_data["type"], validated_data["features"] ))
            print("validated_data")
            print(validated_data)
            return self.model["model"].objects.create(**validated_data)
        def update(slf, instance, validated_data):
            validated_data["features"]=json.loads(validated_data["features"])
            validated_data.update(CG(validated_data["type"], validated_data["features"] ))
            print("validated_data")
            print(validated_data)
            for key, value in validated_data.items():
                setattr(instance, key, value) 
            instance.save()
            print(instance)
            return instance
        return {"create":create,"update":update}

    @property
    def fSerializer(self):
        mdP=cst.models["projects"]
        data={
                "project":UserRelatedField(queryset= mdP["model"].objects.all()),
                "Meta":type("Meta", (object,),{"model": self.model["model"],"fields" : ('url', 'id','project','modified_date',*self.model["fields"])   }),
            }
        if "models" in self.model:
            for (k,v) in self.model["models"].items():  
                md=cst.models[v]
                data[k]=ProjectRelatedField(queryset=md["model"].objects.all())
        if self.name == "sections":
            Save=self.saveSection
            data['features']=serializers.JSONField()
            data["create"]=Save["create"]
            data["update"]=Save["update"]
        return type(self.model["name"]+"Serializer",(serializers.ModelSerializer,),data)
    @property
    def applySerializer(self):
        data={ 
            "project":UserRelatedField(queryset=mds.Project.objects.all()),
            "lst" : serializers.CharField(label="List of "+self.apply),
            "action" : serializers.ChoiceField(default="apply",choices=[("apply", "apply"),('remove', 'remove'),]),
            "save":self.saveApply,
        }
        return type(self.model["name"]+"applySerializer",(serializers.Serializer,),data)

ISerializer={}
for k in cst.lst:
    ISerializer[k]=CSerializer(k)


class ProjectSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = mds.Project
        fields = ('url', 'id', 'name', 'user','auth','modified_date')
          
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'projects')

