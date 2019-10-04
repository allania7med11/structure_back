from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets,filters,serializers
from rest_framework.response import Response
from . import filters as flts
from .permissions import IsUser,IsProject
from . import serializers as srls
from rest_framework import status
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project
from .infs import cst
from . import models as mds      
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from graph.schema import schema
from graph.queries import qProject
@action(detail=True, methods=['post'])
def apply(self, request, pk=None):
    print(request)
    serializer_class_apply=self.get_serializer_class()
    serializer_apply = serializer_class_apply(data=request.data,context={'request': self.request,"pk":pk})
    if serializer_apply.is_valid():
        instance=serializer_apply.save()
        serializer_class=srls.ISerializer[self.nam].fSerializer
        serializer = serializer_class(instance,context={'request': self.request})
        return Response({"serializer.data":serializer.data})
    return Response(serializer.errors, status=400) 
@apply.mapping.get
def apply_get(self, request, pk=None):
    serializer_class=srls.fSerializer(self.nam,user=self.request.user)
    instance=self.model["model"].objects.get(id=7)
    serializer = serializer_class(instance,context={'request': self.request})
    return Response({"serializer.data":serializer.data})    
""" @apply.mapping.get
def retrieve_apply(self, request, pk=None):
    return Response({"message":"hi"}) """

def fViewSet(nam):
    model= cst.models[nam]
    def get_queryset(self):
        queryset = self.model["model"].objects.filter(project__user=self.request.user)
        return queryset    
    def get_serializer_class(self, pk=None):
        queryset = mds.Project.objects.filter(user=self.request.user)
        self.filterset_class=flts.fFilter(self.nam,queryset=queryset)
        if self.action=="apply":
            return srls.applySerializer(self.nam)   
        return srls.fSerializer(self.nam,user=self.request.user)
    data={
        "nam":nam,
        "model":model,
        "permission_classes" : (permissions.IsAuthenticated,IsProject ),
        "filter_backends" : [DjangoFilterBackend,filters.OrderingFilter],
        "filterset_class":flts.fFilter(nam),
        "ordering_fields" : ['project'],
        "ordering" : ['-project'],
        "get_queryset":get_queryset,
        "get_serializer_class":get_serializer_class
    } 
    if "apply" in model:
        data.update({
            "apply":apply,
            "apply_get":apply_get
        })
    return type(model["name"]+"ViewSet",(viewsets.ModelViewSet,),data)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = mds.Project.objects.all()
    serializer_class = srls.fProjectSerializer()
    serializer_class_retrieve = srls.fProjectSerializer(action=True)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsUser )
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['auth']
    ordering_fields = ['auth']
    ordering = ['auth']
    def get_queryset(self):
        user = self.request.user
        print("userrr",user)
        if self.request.user.is_authenticated:
            projects = mds.Project.objects.filter(Q(user=self.request.user) | Q(auth="public"))
        else:
            projects = mds.Project.objects.filter(auth="public")
        return projects 
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_class_retrieve
        return super(ProjectViewSet, self).get_serializer_class()   
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
            for field in cst.apply:
                project[field].extend(default[field])    
        return Response(project)

    @action(detail=False)
    def default(self, request, pk=None):
        serializer = self.serializer_class_retrieve(cst.get_default_project(),context={'request': self.request})
        return Response(serializer.data) 
      
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = srls.UserSerializer
    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset
    @action(detail=False)
    def current(self, request, pk=None):
        serializer = self.serializer_class(self.request.user,context={'request': self.request}) 
        return Response(serializer.data)

               