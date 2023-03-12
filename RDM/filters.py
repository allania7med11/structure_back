from django_filters.rest_framework import FilterSet
import django_filters as filters
from . import models as mds
from .infs import cst

def fFilter(name,queryset=None):
    model= cst.models[name]
    if queryset==None:
        queryset = mds.Project.objects.filter(auth="private")
        data={
            "project":filters.ModelChoiceFilter(queryset=queryset),
            "Meta":type("Meta", (object,),{"model": model["model"],"fields" : ['project']  }) 
        } 
    else:
        data={
            "project":filters.ModelChoiceFilter(queryset=queryset),
            "Meta":type("Meta", (object,),{"model": model["model"],"fields" : ['project']  }),
        }   
    return type(model["name"]+"Filter",(FilterSet,),data)             
