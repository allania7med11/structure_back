from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets,filters,serializers
from rest_framework.response import Response
from . import models as mds
from . import filters as flts
from .permissions import IsUser,IsProject
from . import serializers as srls
from rest_framework import status
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from django.contrib.auth.models import User
from . import models as mds
from .models import Project

        
class SupportViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class=flts.fSupportFilter()
    ordering_fields = ['project']
    ordering = ['-project']
    def get_queryset(self):
        queryset = mds.Support.objects.filter(project__user=self.request.user)
        return queryset    
    def get_serializer_class(self):
        queryset = Project.objects.filter(Q(user=self.request.user) | Q(auth="public"))
        self.filterset_class=flts.fSupportFilter(queryset)
        return srls.fSupportSerializer(queryset)
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = mds.Project.objects.all()
    serializer_class = srls.fProjectSerializer()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
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
            return srls.fProjectSerializer(action=True)
        return super(ProjectViewSet, self).get_serializer_class()   
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save(user=instance.user)
        
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        print()
        if hasattr(self.request, 'user'):
           print({"self.request.user":self.request.user})
           queryset = User.objects.filter(id=self.request.user.id)
        else:
            print("Not logged in")
            queryset = User.objects.none()
        return queryset
    def get_serializer_class(self):
        if self.action == 'list':
            return srls.UserSrlList
        if self.action == 'retrieve':
            return srls.UserSrlRetrieve