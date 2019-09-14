from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet,base_name='project')
router.register(r'supports', views.SupportViewSet,base_name='support')
router.register(r'users', views.UserViewSet,base_name='user')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]