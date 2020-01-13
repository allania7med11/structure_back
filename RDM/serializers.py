from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import models
from RDM.infs import cst
from RDM.help.serializers import UserRelatedField, ProjectRelatedField
from RDM import models as mds
from RDM.help.RDM import CG
import json
from django.utils import timezone

class CSerializer:
    def __init__(self, name):
        self.name = name

    @property
    def model(self):
        return cst.models[self.name]

    @property
    def apply(self):
        return self.model.get("apply")

    @property
    def modelApply(self):
        return cst.models[self.apply]

    @property
    def saveApply(self):
        def fct(slf):
            instance = self.model["model"].objects.get(id=slf.context["pk"])
            action = slf.validated_data.pop('action')
            lst = slf.validated_data.pop('lst')
            project = slf.validated_data.pop('project')
            if action == 'apply':
                if lst == "*":
                    qr = self.modelApply["model"].objects.filter(
                        project=project)
                    print(qr)
                else:
                    L = cst.rlist(lst)
                    qr = self.modelApply["model"].objects.filter(
                        project=project, name__in=L)
            elif action == 'remove':
                if lst == "*":
                    qr = getattr(instance, self.apply).filter(project=project)
                else:
                    L = cst.rlist(lst)
                    qr = getattr(instance, self.apply).filter(
                        project=project, name__in=L)
            if instance and qr:
                if action == "apply":
                    getattr(instance, self.apply).add(*qr)
                elif action == 'remove':
                    if "default" in self.model:
                        model_default = cst.get_default(self.name)
                        getattr(model_default, self.apply).add(*qr)
                    else:
                        getattr(instance, self.apply).remove(*qr)
            project.modified_date = timezone.now()
            project.results = False
            project.save()
            return instance
        return fct

    @property
    def validate_features(self):
        def ftn(slf, value):
            return json.loads(value)
        return ftn

    @property
    def saveModel(self):
        def create(slf, validated_data):
            if self.name == "sections":
                validated_data.update(
                    CG(validated_data["type"], validated_data["features"]))
            instance=self.model["model"].objects.create(**validated_data)
            project=instance.project
            project.modified_date = timezone.now()
            project.results = False
            project.save()
            return instance

        def update(slf, instance, validated_data):
            if self.name == "sections":
                validated_data.update(
                    CG(validated_data["type"], validated_data["features"]))
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            project=instance.project
            project.modified_date = timezone.now()
            project.results = False
            project.save()
            return instance
        return {"create": create, "update": update}

    @property
    def fSerializer(self):
        mdP = cst.models["projects"]
        Save = self.saveModel
        data = {
            "project": UserRelatedField(queryset=mdP["model"].objects.all()),
            "create": Save["create"],
            "update": Save["update"],
            "Meta": type("Meta", (object,), {"model": self.model["model"], "fields": ('url', 'id', 'project', 'modified_date', *self.model["fields"])}),
        }
        if "models" in self.model:
            for (k, v) in self.model["models"].items():
                md = cst.models[v]
                data[k] = ProjectRelatedField(
                    queryset=md["model"].objects.all())
        if "features" in self.model["fields"]:
            data['features'] = serializers.JSONField()
            data['validate_features'] = self.validate_features
        return type(self.model["name"]+"Serializer", (serializers.ModelSerializer,), data)

    @property
    def applySerializer(self):
        data = {
            "project": UserRelatedField(queryset=mds.Project.objects.all()),
            "lst": serializers.CharField(label="List of "+self.apply),
            "action": serializers.ChoiceField(default="apply", choices=[("apply", "apply"), ('remove', 'remove'), ]),
            "save": self.saveApply,
        }
        return type(self.model["name"]+"applySerializer", (serializers.Serializer,), data)


ISerializer = {}
for k in cst.lst:
    ISerializer[k] = CSerializer(k)


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = mds.Project
        fields = ('url', 'id', 'name', 'user', 'auth', 'modified_date')


class CUserSerializer:
    model = User
    fields = ('url', 'id', 'username')
    @property
    def fSerializer(self):
        data = {"Meta": type("Meta", (object,), {
                             "model": self.model, "fields": self.fields}), }
        return type("UserSerializer", (serializers.ModelSerializer,), data)

    @property
    def contactSerializer(self):
        data = {
            "from_email": serializers.EmailField(),
            "subject": serializers.CharField(),
            "message": serializers.CharField()
        }
        return type("contactSerializer", (serializers.Serializer,), data)


class ContactForm(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()


IUserSerializer = CUserSerializer()
