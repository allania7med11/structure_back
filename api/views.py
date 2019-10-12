from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets,filters,serializers
from rest_framework.response import Response
from . import filters as flts
from .permissions import IsUser,IsProject
from api.serializers import ISerializer,ProjectSerializer,UserSerializer
from rest_framework import status
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from django.contrib.auth.models import User
from .infs import cst
from . import models as mds      
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from graph.schema import schema
from graph.queries import qProject,qApply
from api.help.cl import fRun
from django.core.exceptions import ValidationError

class CViewSet:
    def __init__(self, name):
        self.name = name
    @property    
    def model(self):
        return cst.models[self.name]
    @property    
    def srl(self):
        return ISerializer[self.name]
    @property
    def get_queryset(self):
        def flt(slf, pk=None):
            queryset = self.model["model"].objects.filter(project__user=slf.request.user)
            return queryset
        return flt   
    @property    
    def get_serializer_class(self):
        def flt(slf, pk=None):
            if slf.action=="apply":
                return self.srl.applySerializer 
            return self.srl.fSerializer
        return flt
    @property    
    def apply(self):
        retrieve=self.retrieve
        @action(detail=True, methods=['post'])
        def apply(slf, request, pk=None):
            print(request)
            serializer_class_apply=self.srl.applySerializer
            serializer_apply = serializer_class_apply(data=request.data,context={'request': slf.request,"pk":pk})
            if serializer_apply.is_valid():
                serializer_apply.save()
                return retrieve(slf,request, pk=None)
            return Response(serializer_apply.errors, status=400)
        @apply.mapping.get
        def apply_get(slf, request, pk=None):
            return retrieve(slf,request, pk=None)
        return {"apply":apply,"apply_get":apply_get}
    @property    
    def retrieve(self):
        def flt(slf, request, pk=None):
            instance=slf.get_object()
            result = schema.execute(qApply(self.name[:-1],self.model["apply"]),variables={'id': instance.id,'idU': request.user.id},)   
            print(result)
            return Response(result.data[self.name[:-1]])
        return flt
    @property 
    def fViewSet(self):
        data={
            "permission_classes" : (permissions.IsAuthenticated,IsProject ),
            "filter_backends" : [DjangoFilterBackend,filters.OrderingFilter],
            "ordering_fields" : ['project'],
            "ordering" : ['-project'],
            "get_queryset":self.get_queryset,
            "get_serializer_class":self.get_serializer_class,
        } 
        if "apply" in self.model:
            Apply=self.apply
            data.update({
                "apply":Apply["apply"],
                "apply_get":Apply["apply_get"]
            })
        return type(self.model["name"]+"ViewSet",(viewsets.ModelViewSet,),data)
      
IViewSet={}
for k in cst.lst:
    IViewSet[k]=CViewSet(k)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = mds.Project.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsUser )
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['auth']
    ordering_fields = ['auth']
    ordering = ['auth']
    def get_queryset(self):
        projects = mds.Project.objects.filter(user=self.request.user)
        return projects  
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save(user=instance.user)
    def retrieve(self, request, pk=None):
        result = schema.execute(qProject,variables={'id': pk},)
        project=result.data["project"]
        default=result.data["default"]
        if pk!='1':
            for field in cst.default:
                project[field].extend(default[field])    
        return Response(project)
    @action(detail=True)
    def run(self, request, pk=None):
        try:
            e = fRun(pk)
            print(e)
            if e == False:
                return Response({"error":True})
            else:
                return self.retrieve(request, pk)
        except ValidationError as e:
            return Response({"error":e})
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset
    @action(detail=False)
    def current(self, request, pk=None):
        serializer = self.serializer_class(self.request.user,context={'request': self.request}) 
        return Response(serializer.data)

               