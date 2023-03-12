from django.contrib.auth.models import User
from rest_framework import serializers
from RDM import models as mds
from RDM.infs import cst

class UserRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(UserRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(user=request.user)
class ProjectRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(ProjectRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(project__user=request.user)
