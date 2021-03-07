from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.views.static import serve
from django.utils import timezone
from datetime import datetime

from api.models.users.models import CustomUsers
from api.utils.decorators import permissionChecker,permissionCheckerFunc,errorCatch
from api.utils.apiFeatures import APIFeatures
from api.serializers.userSerializer import UserSerializer
from api.serializers.loginSerializer import LoginSerializer


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@errorCatch
def changePassword(request):   
    data=request.data
    if request.user.check_password(data['currentPassword']):
        request.user.set_password(data['newPassword'])
        request.user.save()
        token=Token.objects.get(user=request.user)
        token.delete()
        token=Token.objects.create(user=request.user) 
        return Response({"message":"Password changed successfully","token": token.key,"role":request.user.role
    },status="200")
    return Response({"message":"Action failed, retry later"},status="401")


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@errorCatch
@permissionCheckerFunc("admin")
def signup(request):
    request.data['is_active']=True
    serializer=UserSerializer(data=request.data)
    serializer.is_valid()
    user=serializer.save()
    return Response({"message": "Successfully signed in"})



class LoginAuthToken(ObtainAuthToken):
    @errorCatch
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        user=serializer.validated_data
        user.last_login=datetime.now(tz=timezone.utc)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key, 
            "role":user.role
        }) 

class UserInfo(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        User=get_user_model()
        queryset=APIFeatures(User,request).filter().sort().paginate().limitFields()
        #queryset=queryset.data.fields.remove('password')
        data=queryset.extract()
        criticalFields=['password','passwordResetToken','passwordResetTime']
        for i in data:
            for field in criticalFields:           
                i.pop(field)
        return Response(data=data)       

def createSuperUser(request):
    
    obj = CustomUsers(name='Dhiwakar Nagarajan',first_name='Dhiwakar',last_name='Nagarajan',email='iamdhiwakar@gmail.com',password='pass1234',is_staff=True,is_active=True,is_superuser=True,role='admin')
    obj.set_password('password')#enter your admin password here
    obj.save()