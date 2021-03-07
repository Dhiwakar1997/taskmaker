from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import authentication, permissions
from api.utils.decorators import permissionChecker,errorCatch
from django.views.static import serve

@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@errorCatch
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)