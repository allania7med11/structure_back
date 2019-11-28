from django.db import models
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User

class Project(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='projects')
    auth = models.CharField(max_length=10,default="private",choices=[("private", "private"),("public", "public"),])
    results = models.BooleanField(default=False)
    class Meta:
        unique_together = (("name","user"),)
    def __str__(self):
        y=self.name
        return y

class Support(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    project =models.ForeignKey(Project,on_delete=models.CASCADE,related_name='supports')
    name= models.CharField(max_length=200)
    UX = models.BooleanField()
    UZ = models.BooleanField()
    RY = models.BooleanField()
    class Meta:
        unique_together = (("name", "project"),)
    def __str__(self):
        y=self.name
        return y

def df_json(): return {}
def df_ar3(): return [[0] for i in range(3)]
def df_fl3(): return [0 for i in range(3)]
def df_ch2(): return ["0" for i in range(2)]
def df_ch3(): return ["0" for i in range(3)]
def df_chm2(): return ["0;0" for i in range(2)]
def df_chm3(): return ["0;0" for i in range(3)]
class Node(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    project =models.ForeignKey(Project,on_delete=models.CASCADE,related_name='nodes')
    Support = models.ForeignKey(Support,related_name='nodes',on_delete=models.SET_DEFAULT,default=1 )
    name = models.PositiveIntegerField()
    X = models.FloatField()
    Z = models.FloatField()
    Fn = ArrayField(models.FloatField(), default=df_fl3)
    Dp = ArrayField(models.FloatField(), default=df_fl3)
    Rc = ArrayField(models.FloatField(), default=df_fl3)
    class Meta:
        unique_together = (("name", "project"),)

    def __str__(self):
        return str(self.name)

class Pl(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='pls')
    name = models.CharField(max_length=200)
    FX = models.FloatField(default=0)
    FZ = models.FloatField(default=0)
    CY = models.FloatField(default=0)
    nodes = models.ManyToManyField(Node, blank=True, related_name='pls')

    class Meta:
        unique_together = (("name", "project"),)

    def __str__(self):
        y = self.name
        return y

class Release(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='releases')
    name = models.CharField(max_length=200)
    UX1 = models.BooleanField()
    UZ1 = models.BooleanField()
    RY1 = models.BooleanField()
    UX2 = models.BooleanField()
    UZ2 = models.BooleanField()
    RY2 = models.BooleanField()

    class Meta:
        unique_together = (("name", "project"),)

    def __str__(self):
        y = self.name
        return y

class Material(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='materials')
    name = models.CharField(max_length=200)
    YM = models.FloatField()
    Density = models.FloatField(default=0)

    class Meta:
        unique_together = (("name", "project"),)

    def __str__(self):
        y = self.name
        return y

class Section(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=200)
    material = models.ForeignKey(
        Material, related_name='sections', on_delete=models.SET_DEFAULT, default=1)
    Ax = models.FloatField()
    Iy = models.FloatField()
    H = models.FloatField()
    Cy = models.FloatField()
    type = models.CharField(max_length=20, default="Custom")
    features = JSONField()

    class Meta:
        unique_together = (("name", "project"),)

    def __str__(self):
        y = self.name
        return y

class Bar(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    project =models.ForeignKey(Project,on_delete=models.CASCADE,related_name='bars')
    name = models.PositiveIntegerField()
    N1= models.ForeignKey(Node,related_name='N1', on_delete=models.CASCADE)
    N2=  models.ForeignKey(Node,related_name='N2', on_delete=models.CASCADE)
    Release = models.ForeignKey(
        Release, related_name='bars', on_delete=models.SET_DEFAULT, default=1)
    Section = models.ForeignKey(
        Section, related_name='bars', on_delete=models.SET_DEFAULT, default=1)
    L = models.FloatField(default=0)
    Ch = ArrayField(models.CharField(max_length=20000),
                    default=df_ch3)
    Qg = ArrayField(models.FloatField(), default=df_fl3)
    Ql = ArrayField(models.FloatField(), default=df_fl3)
    Rg = ArrayField(models.FloatField(), default=df_fl3)
    Rl = ArrayField(models.FloatField(), default=df_fl3)
    EF = JSONField(default=df_json)
    DP = JSONField(default=df_json)
    S =  JSONField(default=df_json)
    EFm = JSONField(default=df_json)
    DPm = JSONField(default=df_json)
    Sm = JSONField(default=df_json)


    class Meta:
        unique_together = (("name", "project"),)

    def __str__(self):
        y = str(self.name)
        return y

class Dl(models.Model):
    modified_date = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='dls')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    Axes = models.CharField(max_length=1, choices=(
        ('G', 'Global'), ('L', 'Local'),), default="G")
    features = JSONField()
    bars = models.ManyToManyField(
        Bar, blank=True, related_name='dls')

    class Meta:
        unique_together = (("name", "project"),)

    def __str__(self):
        y = self.name
        return y


class Task(models.Model):
    isDone = models.BooleanField()
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
  	pass

""" 
choices=[("RCT", "Rectangular"),("RCTH", "Rectangular Hollow"),
                 ("CRC", "Circular"),("CRCH", "Circular Hollow"),
                 ("TSC", "T Section"),("ISC", "I Section"),
                 ("CST", "Custom"),
                 ]
                  """