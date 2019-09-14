from django_filters.rest_framework import FilterSet
import django_filters as filters
from . import models as mds


def fSupportFilter(queryset=None):
    if queryset==None:
        queryset = mds.Project.objects.filter(auth="private")
        data={
            "project":filters.ModelChoiceFilter(queryset=queryset),
            "Meta":type("Meta", (object,),{"model": mds.Support,"fields" : ['project']  }) 
        } 
    else:
        data={
            "project":filters.ModelChoiceFilter(queryset=queryset),
            "Meta":type("Meta", (object,),{"model": mds.Support,"fields" : ['project']  }),
        }         
    SupportFilter=type("SupportFilter",(FilterSet,),data) 
    return SupportFilter       