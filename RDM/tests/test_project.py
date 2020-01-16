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
    
    
    def test_run(self):
        user = cst.get_default_user
        self.client.login(username="allania7med11", password='Ahmed.va.2000')
        for tutorial in cst.project["Tutorials"]:
            project = Project.objects.get(user=user, name=tutorial)
            path = "/api/projects/{}/run/".format(project.id)  
            response = self.client.get(path)
            assert response.status_code == 200
