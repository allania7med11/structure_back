from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from api.views import ProjectViewSet,UserViewSet,IViewSet
from .infs import cst
router = DefaultRouter()
router.register(r'projects', ProjectViewSet,'project')
router.register(r'users', UserViewSet,'user')

for k in cst.lst:
    router.register(rf'{k}', IViewSet[k].fViewSet,k[:-1])
 
urlpatterns = [
    url(r'^', include(router.urls)),
]