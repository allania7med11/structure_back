from . import models as mds

class cst(object):
    lst=["nodes","bars","supports","releases"]
    models={
        "nodes": {"model": mds.Node, "name": "Node", "fields": ["name","X","Z"]},
        "bars": {"model": mds.Bar, "name": "Bar", "fields": ["name",'N1', 'N2'],"models": {"N1": "nodes", "N2": "nodes"}},
        "supports": {"model": mds.Support, "name": "Support", "fields": ["name",'UX', 'UZ','RY']},
        "releases": {"model": mds.Release, "name": "Release", "fields": ["name","UX1", "UZ1", "RY1", "UX2", "UZ2", "RY2"]},
    }