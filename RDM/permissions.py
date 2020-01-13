from rest_framework import permissions
from . import models as mds

class IsUser(permissions.BasePermission):
    message = 'You don\'t own this project'
    def has_object_permission(self, request, view, obj): 
        if obj.user == request.user:
            return True
        return obj.auth=="public" and request.method in permissions.SAFE_METHODS
        
class IsProject(permissions.BasePermission):
    message = 'You don\'t own this project'
    def has_object_permission(self, request, view, obj):
        return obj.project.user == request.user
       
        