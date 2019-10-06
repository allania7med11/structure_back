from django.contrib.auth.models import User
import graphene_django_extras as extras

from graphene_django_extras import DjangoListObjectType, DjangoSerializerType, DjangoObjectType
from api.models import Project
from api.infs import cst
class CType:
    def __init__(self, name):
        self.name = name
    @property    
    def model(self):
        return cst.models[self.name]
    @property
    def fType(self):
        data={
            "Meta":type("Meta", (object,),{
                "model": self.model["model"],
                'filter_fields':{"id": ("exact", ),"project": ("exact", ),}   
            }),
        }
        return type(self.model["name"]+"Type",(extras.DjangoObjectType,),data)
    @property
    def fListType(self):
        data={
                "Meta":type("Meta", (object,),{
                    "model": self.model["model"],
                }),
            }
        return type(self.model["name"]+"ListType",(extras.DjangoListObjectType,),data)
IType={}
for k in cst.lst:
    IType[k]=CType(k)
class CProjectType:
    @property    
    def model(self):
        return cst.models["projects"]
    @property
    def fType(self):
        data={
            "Meta":type("Meta", (object,),{
                "model": self.model["model"],
                'filter_fields':{"id": ("exact", ),}   
            }),
        }
        return type(self.model["name"]+"Type",(extras.DjangoObjectType,),data)
    @property
    def fListType(self):
        data={
                "Meta":type("Meta", (object,),{
                    "model": self.model["model"],
                 }),
            }
        return type(self.model["name"]+"ListType",(extras.DjangoListObjectType,),data)
IType["projects"]=CProjectType()
""" class ProjectType(DjangoObjectType):
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
        model = Release """