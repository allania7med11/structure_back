from RDM.models import Support,Node,Project
instance= Support.objects.get(id=7)
qr = getattr(instance,"nodes").filter(project=instance.project)
project=Project.objects.get(user__username="allania7med11",name="Default")
Support_default = Support.objects.get(project=project,name="None")
getattr(Support_default,"nodes").add(*qr)
