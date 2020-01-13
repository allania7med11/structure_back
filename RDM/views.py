from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, filters
from rest_framework.response import Response
from RDM.serializers import ISerializer, ProjectSerializer, IUserSerializer
from .permissions import IsUser, IsProject
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from django.contrib.auth.models import User
from .infs import cst
from . import models as mds
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from graph.schema import schema
from graph.queries import Queries
from RDM.help.cl import fRun
from RDM.help.copy import Copy
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from RDM import models as mds

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
            if slf.action == "apply":
                return self.srl.applySerializer
            return self.srl.fSerializer
        return flt

    @property
    def apply(self):
        retrieve = self.retrieve
        @action(detail=True, methods=['post'])
        def apply(slf, request, pk=None):
            print(request)
            serializer_class_apply = self.srl.applySerializer
            serializer_apply = serializer_class_apply(
                data=request.data, context={'request': slf.request, "pk": pk})
            if serializer_apply.is_valid():
                serializer_apply.save()
                return retrieve(slf, request, pk=None)
            return Response(serializer_apply.errors, status=400)

        @apply.mapping.get
        def apply_get(slf, request, pk=None):
            return retrieve(slf, request, pk=None)
        return {"apply": apply, "apply_get": apply_get}

    @property
    def retrieve(self):
        def flt(slf, request, pk=None):
            instance = slf.get_object()
            result = schema.execute(Queries.apply(
                self.name[:-1], self.model["apply"]), variables={'id': instance.id, 'idU': request.user.id},)
            print(result)
            return Response(result.data[self.name[:-1]])
        return flt

    @property
    def fViewSet(self):
        data = {
            "permission_classes": (permissions.IsAuthenticated, IsProject),
            "filter_backends": [DjangoFilterBackend, filters.OrderingFilter],
            "ordering_fields": ['project'],
            "ordering": ['-project'],
            "get_queryset": self.get_queryset,
            "get_serializer_class": self.get_serializer_class,
        }
        if "apply" in self.model:
            Apply = self.apply
            data.update({
                "apply": Apply["apply"],
                "apply_get": Apply["apply_get"]
            })
        return type(self.model["name"] + "ViewSet",
                    (viewsets.ModelViewSet,), data)


IViewSet = {}
for k in cst.lst:
    IViewSet[k] = CViewSet(k)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = mds.Project.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUser )
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['auth']
    ordering_fields = ['auth']
    ordering = ['auth']

    def get_serializer_class(self):
        if self.action == "copy":
            return Copy.copySerializer
        return self.serializer_class

    def get_queryset(self):
        projects = mds.Project.objects.filter(user=self.request.user)
        return projects

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save(user=instance.user)

    def get_project(self, id):
        result = schema.execute(Queries.project, variables={'id': id},)
        project = result.data["project"]
        default = result.data["default"]
        if id != '1':
            for field in cst.default:
                project[field].extend(default[field])
        return project

    def retrieve(self, request, pk=None):
        project = self.get_project(pk)
        return Response(project)

    @action(detail=False)
    def Tutorials(self, request):
        name = self.request.query_params.get('name', False)
        projects = {}
        List = cst.get_Tutorials
        if (name):
            List = list(filter(lambda x: x["name"] == cst.urlsI[name], List))
        for item in List:
            name = cst.project["urls"][item["name"]]
            projects[name] = self.get_project(item["id"])
        return Response(projects)

    @action(detail=True)
    def run(self, request, pk=None):
        try:
            e = fRun(pk)
            print(e)
            if not e:
                return Response({"error": True})
            else:
                projectI =mds.Project.objects.get(id = pk)
                projectI.results = True
                projectI.save()
                result = schema.execute(Queries.results, variables={'id': pk},)
                project = result.data["project"]
                default = result.data["default"]
                if pk != '1':
                    project["sections"].extend(default["sections"])
                return Response(project)
        except ValidationError as e:
            return Response({"error": e})

    @action(detail=True, methods=['post'])
    def copy(self, request, pk=None):
        try:
            prc = schema.execute(Queries.copy, variables={'id': pk},)
            print("prc", prc.data)
            context = {'request': request, "pk": pk,
                       "data": prc.data["project"]}
            print("context", context)
            serializer_class_copy = Copy.copySerializer
            serializer_copy = serializer_class_copy(
                data=request.data, context=context)
            if serializer_copy.is_valid():
                print("serializer_copy", serializer_copy)
                instance = serializer_copy.save()
                print("instance", instance)
            return self.retrieve(request, pk)
        except ValidationError as e:
            return Response({"error": e})

    @copy.mapping.get
    def copy_get(self, request, pk=None):
        return Response({"tese": "test"})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = IUserSerializer.fSerializer

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset

    def get_serializer_class(self):
        if self.action == "contact":
            return IUserSerializer.contactSerializer
        return self.serializer_class

    @action(detail=False)
    def current(self, request, pk=None):
        serializer = self.serializer_class(
            self.request.user, context={'request': self.request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def contact(self, request, pk=None):
        serializer_class_contact = IUserSerializer.contactSerializer
        serializer_contact = serializer_class_contact(
            data=request.data, context={'request': self.request})
        if serializer_contact.is_valid():
            subject = serializer_contact.validated_data['subject']
            from_email = serializer_contact.validated_data['from_email']
            message = serializer_contact.validated_data['message']
            try:
                send_mail(subject, message, from_email,
                          ['allania7med11@gmail.com'])
            except BadHeaderError:
                return Response({"error": 'Invalid header found.'})
            return Response({"msg": 'Success'})
        return Response(serializer_contact.errors, status=400)
