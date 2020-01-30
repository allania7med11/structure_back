from rest_framework import permissions
from . import models as mds
from server import env
from .infs import cst
class TestOnly(permissions.BasePermission):
    message = 'permission denied'
    def has_permission(self, request, view):
        return env.Test
class IsUser(permissions.BasePermission):
    message = 'You don\'t own this project'
    def has_object_permission(self, request, view, obj): 
        if obj.user == request.user:
            return True
        return obj.auth=="public" and request.method in permissions.SAFE_METHODS
        
class IsProject(permissions.BasePermission):
    message = 'You don\'t own this project'
    def has_object_permission(self, request, view, obj):
        if obj.project.user == request.user:
            return True
        return obj.project == cst.get_default_project
       
        