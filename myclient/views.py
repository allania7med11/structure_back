from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.

@ensure_csrf_cookie
def auth(request):
    return HttpResponse(status=200)