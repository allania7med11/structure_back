from api.models import Support,Node,Project
print("hello")
instance= Support.objects.get(id=7)
print(instance)
qr = getattr(instance,"nodes").filter(project=instance.project)
print(qr)
project=Project.objects.get(user__username="allania7med11",name="Default")
Support_default = Support.objects.get(project=project,name="None")
print(getattr(instance,"nodes"))
print(getattr(Support_default,"nodes"))
getattr(Support_default,"nodes").add(*qr)
print("Now")
print(getattr(instance,"nodes"))
print(getattr(Support_default,"nodes"))