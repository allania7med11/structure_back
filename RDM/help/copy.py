import json
from RDM import models as mds
from RDM.help.RDM import CG
from rest_framework import serializers
class cCopy(object):
    one={"Support":mds.Support,"N1":mds.Node,"N2":mds.Node,
     "Release":mds.Release,"material":mds.Material,"Section":mds.Section}
    many={"nodes":mds.Node,"bars":mds.Bar}
    models={
        "projects":mds.Project,"nodes":mds.Node,"bars":mds.Bar,"supports":mds.Support,
        "releases":mds.Release,"materials":mds.Material,"sections":mds.Section,
        "pls":mds.Pl,"dls":mds.Dl    }
    List=["supports","releases","materials","sections","nodes","bars","pls","dls"]
    def conv(self,project,model,args):
        ds={'project': project}
        print("model",model,args)
        if model=="sections":
            args.update(CG(args["type"], json.loads(args["features"])))
        for k,v in args.items():
            if k in self.one.keys():
                ds[k]=self.one[k].objects.get(project__id__in=[1,project.id],name=v["name"])
            elif not(k in self.many.keys() or k=="features") :
                ds[k]=v
            elif k=="features" :
                ds[k]=json.loads(v)
        print("ds",ds)
        ins = self.models[model].objects.create(**ds)
        for k in [ki for ki in self.many.keys() if ki in args.keys()]:
            list=[v["name"] for v in  args[k]]
            getattr(ins, k).add(*self.many[k].objects.filter(project=project, name__in=list))  
        return ins
    @property
    def saveCopy(self):
        def fct(slf):
            name= slf.validated_data.pop('name')
            print("name",name)
            data=slf.context["data"]
            prc=mds.Project.objects.get(id=slf.context["pk"])
            prn=mds.Project.objects.create(name=name,user=prc.user)
            print(data)
            for model in self.List:
                print(model)
                for args in data[model]:
                    instance=self.conv(prn,model,args)
            return prn
        return fct
    @property
    def copySerializer(self):
        data={"name" : serializers.CharField(label="Name"),"save":self.saveCopy}
        return type("copySerializer",(serializers.Serializer,),data)
Copy=cCopy()