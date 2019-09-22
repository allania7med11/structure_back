from . import models as mds

class cst(object):
    models={
        "nodes": {"model": mds.Node, "name": "Node", "fields": ["name","X","Z"]},
        "supports": {"model": mds.Support, "name": "Support", "fields": ["name",'UX', 'UZ','RY']},
    }