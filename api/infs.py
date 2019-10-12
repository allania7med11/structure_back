from . import models as mds
import re
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
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
    @staticmethod
    def get_default_project():
        return mds.Project.objects.get(user__username="allania7med11",name="Default")         
    @classmethod
    def get_default(cls,name):
        model=cls.models[name]
        project=cls.get_default_project()
        return model["model"].objects.get(project=project,name=model["default"])    
    
cst=Classcst()