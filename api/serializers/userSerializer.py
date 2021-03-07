from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from api.models.users.models import CustomUsers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #profile_pic= serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance,attr,value)
        instance.save()
        return instance
    class Meta:
        model = CustomUsers
        extra_kwargs ={'password':{'write_only':True}}
        fields =['name','email','password','phone','gender','is_active','is_staff','is_superuser','first_name','last_name','profile_pic','role']
