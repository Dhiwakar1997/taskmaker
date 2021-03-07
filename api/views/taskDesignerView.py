from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from api.models.tasks.models import Task
from api.utils.decorators import permissionChecker
from api.utils.apiFeatures import APIFeatures
from api.serializers.taskSerializer import TaskSerializer

from django.utils import timezone
from datetime import datetime

class DesignerTaskManager(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @permissionChecker('designer')
    def get(self,request,id,format=None):
        task=Task.objects.get(id=id)
        if task.status=='assigned':
            task.startedTime=datetime.now(tz=timezone.utc)
            task.status='started'
            task.save()
            print("started")
        queryset=Task.objects.filter(id=task.id)      
        serializer=TaskSerializer
        serializer.Meta.fields=['name','description','workFiles','status','startedTime','admin_id','QC_id']
        obj=serializer(data=queryset,many=True,context={"request":request})
        obj.is_valid()
        return Response(data=obj.data)
    
    @permissionChecker('designer')
    def post(self, request,id,format=None):
        task=Task.objects.get(id=id)
        serializer=TaskSerializer
        request.data['status']='submitted'
        request.data['submittedTime']=datetime.now(tz=timezone.utc)
        serializer.Meta.fields=['submittedFiles','submittedTime','status']
        obj=serializer(instance=task,data=request.data)
        obj.is_valid()
        obj.save()
        return Response('submitted')


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def currentDesignerTask(request):
    statusQuery= r'^assigned$|^started$'
    if 'status' in request.query_params:
        statusQuery= request.query_params['status'] 
    tasks=Task.objects.filter(designer_id=request.user.id,status__regex=statusQuery).order_by('-assignedTime','-id')
    serializer=TaskSerializer
    serializer.Meta.fields='__all__'
    obj=serializer(data=tasks,many=True,context={'request': request})
    obj.is_valid()
    return Response(data=obj.data)
