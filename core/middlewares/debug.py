import logging

from django.urls import resolve

logger = logging.getLogger(__name__)


class DebugMiddleware:
    """
    This middleware for debugging purpose
    to use this middleware you  need to add  "ACTIVATE_DJANGO_debug_MIDDLEWARE=True" to your .env file
    before making the action you want to investigate in the frontend
    add breakpoint to 'response = self.get_response(request)'
    any request make to the server will hit that line
    * investigate the request object you get from the front end after it was handled by other middlewares
    * step into self.get_response to investigate wich part of code will handled that request
    * investigate the response variable that represent the response returned by the server for that request
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # display request infos
        logger.info(f"Request: {request.method} {request.path}")
        # display view infos
        myfunc, myargs, mykwargs = resolve(request.path)
        mymodule = myfunc.__module__.replace(".", "/")
        myname = myfunc.__name__
        logger.info(f"View: {mymodule} {myname} {myargs} {mykwargs}")
        response = self.get_response(request)
        # Code to be executed for each request/response after
        template_name = getattr(response, "template_name", None)
        if template_name:
            logger.info(f"Response: {template_name}")
        return response