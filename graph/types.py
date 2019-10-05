from django.contrib.auth.models import User
from graphene_django_extras import DjangoListObjectType, DjangoSerializerType, DjangoObjectType
from api.models import Project,Node,Support,Release,Bar

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        description = " Type definition for a single user "
        filter_fields = {
            "id": ("exact", ),
        }
class ProjectListType(DjangoListObjectType):
    class Meta:
        description = " Type definition for user list "
        model = Project

class NodeType(DjangoObjectType):
    class Meta:
        model = Node
        description = " Type definition for a single user "
        filter_fields = {
            "id": ("exact", ),
            "project": ("exact", ),
        }
class NodeListType(DjangoListObjectType):
    class Meta:
        description = " Type definition for user list "
        model = Node

class SupportType(DjangoObjectType):
    class Meta:
        model = Support
        description = " Type definition for a single user "
        filter_fields = {
            "id": ("exact", ),
            "project": ("exact", ),
        }
class SupportListType(DjangoListObjectType):
    class Meta:
        description = " Type definition for user list "
        model = Support
class BarType(DjangoObjectType):
    class Meta:
        model = Bar
        description = " Type definition for a single user "
        filter_fields = {
            "id": ("exact", ),
            "project": ("exact", ),
        }
class BarListType(DjangoListObjectType):
    class Meta:
        description = " Type definition for user list "
        model = Bar
class ReleaseType(DjangoObjectType):
    class Meta:
        model = Release
        description = " Type definition for a single user "
        filter_fields = {
            "id": ("exact", ),
            "project": ("exact", ),
        }
class ReleaseListType(DjangoListObjectType):
    class Meta:
        description = " Type definition for user list "
        model = Release