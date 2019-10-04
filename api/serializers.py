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
            serializer=serializers.HyperlinkedRelatedField(view_name='project-detail',queryset=qs)
            return serializer.data  
        return fct
    @property    
    def get_apply(self):
        def fct(slf, instance):
            request=slf.context["request"]
            print({"user":request.user})
            qs = self.modelApply["model"].objects.filter(**{"project__user":request.user,self.model["name"]:instance})
            serializer=serializers.HyperlinkedRelatedField(view_name='project-detail',queryset=qs,many=True,read_only=True)
            return serializer.data  
        return fct
    def get_(self,md):
        def fct(slf, instance):
            request=slf.context["request"]
            print({"user":request.user})
            qs = md["model"].objects.filter(project__user=request.user)
            serializer=serializers.HyperlinkedRelatedField(view_name='project-detail',queryset=qs,many=True,read_only=True)
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
        return type(self.model["name"]+"Serializer",(serializers.HyperlinkedModelSerializer,),data)
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
ISerializer={}
for k in cst.lst:
    ISerializer[k]=CSerializer(k)
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
                md=cst.models[v]
                data[k]=serializers.SerializerMethodField('get_'+k)
                data["get_"+k]=ISerializer[v].get_(md)        
    else:
        data={
            "project":serializers.HyperlinkedRelatedField(view_name='project-detail',queryset=mds.Project.objects.filter(user=user)),
            "Meta":type("Meta", (object,),{"model": model["model"],"fields" : ('url', 'id','project','modified_date',*model["fields"])   }),
        } 
        if "models" in model:
            for (k,v) in model["models"].items():  
                md=cst.models[v]
                data[k]=serializers.SerializerMethodField('get_'+k)
                data["get_"+k]=ISerializer[v].get_(md)
               
    if "apply" in model:
        data[model["apply"]]=infSerializer(model["apply"])(many=True,read_only=True)            
    return type(model["name"]+"Serializer",(serializers.HyperlinkedModelSerializer,),data)
def Serializer1(name,model,fields):
    data={
            "Meta":type("Meta", (object,),{"model": model,"fields" : ('url', 'id','project','modified_date',*fields)   }) 
        }
    return type(name,(serializers.HyperlinkedModelSerializer,),data) 

class CProjectSerializer:
    def get_(self,k):
        def fct(slf, instance):
            # serializer_class=ISerializer[k].fSerializer()
            model= cst.models[k]
            serializer_class=Serializer1(k+"serializer1",model["model"],model["fields"])
            print(["serializer_class",type(serializer_class)])
            qs = ISerializer[k].model["model"].objects.filter(project=instance)
            serializer=serializer_class(qs,context=slf.context,many=True,read_only=True)
            return serializer.data   
        return fct
    def fSerializer(self):
        data={
            "user" : serializers.ReadOnlyField(source='user.username'),
            **{k:serializers.ListField(read_only=True, child=ISerializer[k].fSerializer() ) for k in cst.lst},
            "Meta":type("Meta", (object,),{"model": mds.Project,"fields" : ('url', 'id', 'name', 'user','auth',*cst.lst)   }),
        }  
        ProjectSerializer=type("ProjectSerializer",(serializers.HyperlinkedModelSerializer,),data) 
        return ProjectSerializer 

IProjectSerializer= CProjectSerializer() 
def fProjectSerializer(action=None):
    if action==None:
        data={
            "user" : serializers.ReadOnlyField(source='user.username'),
            "Meta":type("Meta", (object,),{"model": mds.Project,"fields" : ('url', 'id','modified_date','name', 'user','auth')  }) 
        } 
    else:
        data={
            "user" : serializers.ReadOnlyField(source='user.username'),
            "Meta":type("Meta", (object,),{"model": mds.Project,"fields" : ('url', 'id', 'name', 'user','auth',*cst.lst)   }),
        } 
        for k in cst.lst:  
            data[k]=serializers.SerializerMethodField('get_'+k)
            data["get_"+k]=IProjectSerializer.get_(k)      
    ProjectSerializer=type("ProjectSerializer",(serializers.HyperlinkedModelSerializer,),data) 
    return ProjectSerializer
          


 
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    projects = serializers.HyperlinkedRelatedField(
        many=True, view_name='project-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'projects')

