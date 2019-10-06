from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from api.views import ProjectViewSet,UserViewSet,IViewSet
from .infs import cst
router = DefaultRouter()
router.register(r'projects', ProjectViewSet,base_name='project')
router.register(r'users', UserViewSet,base_name='user')

for k in cst.lst:
    router.register(rf'{k}', IViewSet[k].fViewSet,base_name=k[:-1])
  
urlpatterns = [
    url(r'^', include(router.urls)),
]