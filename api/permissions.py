from rest_framework import permissions
from . import models as mds

class IsUser(permissions.BasePermission):
    message = 'You don\'t own this project'
    def has_object_permission(self, request, view, obj): 
        return obj.user == request.user 
class IsProject(permissions.BasePermission):
    message = 'You don\'t own this project'
    def has_permission(self, request, view):
        print({"HTTP_PROJECT_Pr":request.META["HTTP_PROJECT"]})
        project_id=request.META["HTTP_PROJECT"]
        if project_id is not None:
            try:
                project = mds.Project.objects.get(pk=project_id)
                print(["test",project.user,request.user])
                return project.user == request.user
            except mds.Project.DoesNotExist:
                return False
        return True