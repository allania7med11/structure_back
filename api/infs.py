from . import models as mds
import re
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
class cst(object):
    lst=["nodes","bars","supports","releases"]
    lstP=["projects","nodes","bars","supports","releases"]
    apply=["supports","releases"]
    models={
        "projects": {"model": mds.Project, "name": "Project", "fields": ["name"]},
        "nodes": {"model": mds.Node, "name": "Node", "fields": ["name","X","Z"]},
        "bars": {"model": mds.Bar, "name": "Bar", "fields": ["name",'N1', 'N2'],"models": {"N1": "nodes", "N2": "nodes"}},
        "supports": {"model": mds.Support, "name": "Support", "fields": ["name",'UX', 'UZ','RY',"nodes"],"apply":"nodes","default":"None"},
        "releases": {"model": mds.Release, "name": "Release", "fields": ["name","UX1", "UZ1", "RY1", "UX2", "UZ2", "RY2","bars"],"apply":"bars","default":"None"},
    }
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
    @staticmethod
    def get_default_project():
        return mds.Project.objects.get(user__username="allania7med11",name="Default")         
    @classmethod
    def get_default(cls,name):
        model=cls.models[name]
        project=cls.get_default_project()
        return model["model"].objects.get(project=project,name=model["default"])    
    
    