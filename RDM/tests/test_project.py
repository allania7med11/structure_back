from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from RDM.models import Project
from mixer.backend.django import mixer
import pytest
from RDM.infs import cst
from django.test import Client
from django.core.management import call_command



class TestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        call_command('loaddata', 'RDM/json/user.json')
        call_command('loaddata', 'RDM/json/RDM.json')
        cls.user = mixer.blend(User, username="user1")
        cls.user.set_password('Puser1')
        cls.user.save()
        cls.client = Client()
        cls.session = cls.client.session
        cls.session.save()
    
    def typProject(self,name):
        path = "/api/projects/"
        response = self.client.post(path,{'name':name})
        assert response.status_code in [200,201]
        response = self.client.get(path)
        assert response.status_code == 200
        assert Project.objects.filter(**{'name':name}).count() > 0
        return Project.objects.get(name=name)

    def test_project_open_owner(self):
        self.client.login(username="user1", password='Puser1')
        self.project=self.typProject("testProject")
        path = "/api/projects/"
        response = self.client.get(path)
        assert response.status_code == 200
        self.DataProject=cst.DataProject(self.project.id)
        for model in cst.lst:
            path = "/api/{}/".format(model)  
            inf=cst.models[model]
            dts=self.DataProject[model]["define"](1)
            for dt in dts:
                dt.update({"project":self.project.id})
                response = self.client.post(path,dt)
                assert response.status_code in [200,201]
                assert inf["model"].objects.filter(project=self.project,name=dt["name"]).count() > 0
    def test_run(self):
        user = cst.get_default_user
        self.client.login(username="allania7med11", password='Ahmed.va.2000')
        for tutorial in cst.project["Tutorials"]:
            project = Project.objects.get(user=user, name=tutorial)
            path = "/api/projects/{}/run/".format(project.id)  
            response = self.client.get(path)
            assert response.status_code == 200
