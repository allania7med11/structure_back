from . import models as mds
import re
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from django.contrib.auth.models import User
import json
class Classcst(object):
    lst=["nodes","bars","supports","releases","materials","sections","pls","dls"]
    apply=["supports","releases","sections","pls","dls"]
    default=["supports","releases","sections","materials"]
    models={
        "projects": {"model": mds.Project, "name": "Project", "fields": ["name"]},
        "nodes": {"model": mds.Node, "name": "Node", "fields": ["name","X","Z"]},
        "bars": {"model": mds.Bar, "name": "Bar", "fields": ["name",'N1', 'N2'],"models": {"N1": "nodes", "N2": "nodes"}},
        "supports": {"model": mds.Support, "name": "Support", "fields": ["name",'UX', 'UZ','RY'],"apply":"nodes","default":"None"},
        "releases": {"model": mds.Release, "name": "Release", "fields": ["name","UX1", "UZ1", "RY1", "UX2", "UZ2", "RY2"],"apply":"bars","default":"None"},
        "materials": {"model": mds.Material, "name": "Material", "fields": ["name",'YM', 'Density']},
        "sections": {"model": mds.Section, "name": "Section", "fields": ["name",'material', 'type','features'],"apply":"bars","default":"Default"},
        "pls": {"model": mds.Pl, "name": "Pl", "fields": ["name","FX", "FZ", "CY"],"apply":"nodes"},
        "dls": {"model": mds.Dl, "name": "Dl", "fields": ["name","type", "Axes", "features"],"apply":"bars"},
    }
    project= {
        "model": mds.Project, 
        "username":"allania7med11",
        "default":"Default",
        "Tutorials":["project 1","Truss Structure","Frame Structure","Beams with Internal Hinges"],
        "urls":{
            "project 1":"Beam",
            "Truss Structure":"TrussStructure",
            "Frame Structure":"FrameStructure",
            "Beams with Internal Hinges":"BeamsInternalHinges"
            }
        }
    
    @property
    def urlsI(self):
        return { v:k for (k,v) in self.project["urls"].items()}
    @property
    def lstP(self):
        return [*self.lst,"projects"]
    @staticmethod
    def rlist(st):
        di = re.findall(r'(?:,|^)\s*(\d+)', st)
        df = re.findall(r'(\d+)\s*(?:,|$)', st)
        d = set(di).intersection(df)
        L = list(set([int(v) for v in list(d)]))
        wi = re.findall(r'(\d+)\s*-\s*(\d+)\s*(?:,|$)', st)
        wf = re.findall(r'(?:,|^)\s*(\d+)\s*-\s*(\d+)', st)
        w = set(wi).intersection(wf)
        for v in list(w):
            s = [int(w) for w in v]
            L.extend(list(range(min(s), max(s)+1)))
        L = list(set(L))
        L.sort()
        print({"List":L})
        return L
    @staticmethod
    def get_object(object_name, relayId, otherwise=None):
        try:
            return object_name.objects.get(pk=relayId)
        except ObjectDoesNotExist:
            return otherwise
   
    @property
    def get_default_user(self):
        return User.objects.get(username=self.project["username"])

    @property
    def get_default_project(self):
        return self.project["model"].objects.get(user=self.get_default_user, name=self.project["default"])

    @property
    def get_Tutorials(self):
        return list( self.project["model"].objects.filter(
            user__username=self.project["username"],
            name__in=self.project["Tutorials"]).values('id', 'name') ) 
    def get_default(self,name):
        model=self.models[name]
        project=self.get_default_project
        return model["model"].objects.get(project=project,name=model["default"])    
    @property
    def results(self):
        input_file = open('RDM/json/results.json', 'r')
        json_decode = json.load(input_file)
        return json_decode
cst=Classcst()