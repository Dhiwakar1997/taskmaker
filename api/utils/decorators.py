from rest_framework.response import Response
from .errorHandler import errorResponse
import functools

def permissionChecker(role):
    def decorator(view_func):
        @functools.wraps(view_func)
        def warpperFunction(self,request, *args, **kwargs):
            user_role=request.user.role
            if user_role==role:
                return view_func(self,request, *args, **kwargs)
            else:
                return errorResponse('unauthorized request',"401")
        return warpperFunction
    return decorator

def permissionCheckerFunc(role):
    def decorator(view_func):
        @functools.wraps(view_func)
        def warpperFunction(request, *args, **kwargs):
            user_role=request.user.role
            if user_role==role:
                return view_func(request, *args, **kwargs)
            else:
                return errorResponse('unauthorized request',"401")
        return warpperFunction
    return decorator


def errorCatch(view_func):
    @functools.wraps(view_func)
    def warpperFunction(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Exception as err:
            return errorResponse('Operational error','501')
    return warpperFunction
