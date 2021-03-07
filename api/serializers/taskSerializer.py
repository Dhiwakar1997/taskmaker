from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from api.models.tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    #profile_pic= serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    def create(self, validated_data):    
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
    class Meta:
        model = Task
        fields =['name','description','workFiles','designer_id','admin_id','QC_id','status']

