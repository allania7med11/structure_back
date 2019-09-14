from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from . import models as mds
from .permissions import IsUser,IsProject
from . import serializers as srls

class SupportViewSet(viewsets.ModelViewSet):
    queryset = mds.Support.objects.all()
    serializer_class = srls.SupportSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsProject, )
    def get_queryset(self):
        user = self.request.user
        supports = mds.Support.objects.filter(project__user=user)
        return supports    
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = mds.Project.objects.all()
    serializer_class = srls.ProjectSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsUser, )
    def get_queryset(self):
        user = self.request.user
        projects = mds.Project.objects.filter(user=user)
        return projects    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save(user=instance.user)
        


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    def get_serializer_class(self):
        if self.action == 'list':
            return srls.UserSrlList
        if self.action == 'retrieve':
            return srls.UserSrlRetrieve

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'supports', views.SupportViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls))
]