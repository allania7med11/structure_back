from django.contrib import admin
from .models import *


class NodeAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'name', 'X', "Z")

class BarAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'name', 'N1', "N2")
class SupportAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'name', 'UX', "UZ", "RY")    

class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name', 'UX1',
                    "UZ1", "RY1", 'UX2', "UZ2", "RY2")


class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name', "material", 'type', "features")

class PlAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name', "FX", 'FZ', "CY")

class DlAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name', "Axes", 'type', "features")



class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name', 'YM', "Density")

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'user',"modified_date")
admin.site.register(Node, NodeAdmin)
admin.site.register(Bar, BarAdmin)
admin.site.register(Support, SupportAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Pl, PlAdmin)
admin.site.register(Dl, DlAdmin)
admin.site.register(Project,ProjectAdmin)

