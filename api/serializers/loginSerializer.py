from rest_framework import serializers
from api.models.users.models import CustomUsers

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        """
        Check that start is before finish.
        """
        user=CustomUsers.objects.get(email=data['email'])

        if user.check_password(data['password']):
            return user
        else:
            raise serializers.ValidationError("email id or password is invalid")
   
         
