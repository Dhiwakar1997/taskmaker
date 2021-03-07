from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from api.models.tasks.models import Task
from api.utils.decorators import permissionChecker,permissionCheckerFunc
from api.utils.apiFeatures import APIFeatures
from api.serializers.taskSerializer import TaskSerializer

from django.utils import timezone
from datetime import datetime

class QcTaskManager(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    @permissionChecker('QC')
    def post(self, request,id,format=None):
        task=Task.objects.get(id=id)
        serializer=TaskSerializer
        request.data['status']='completed'
        request.data['approvalTime']=datetime.now(tz=timezone.utc)
        serializer.Meta.fields=['approvalTime','status']
        obj=serializer(instance=task,data=request.data)
        obj.is_valid()
        obj.save()
        return Response({'message':'approved'})
    
    @permissionChecker('QC')
    def delete(self, request,id,format=None):
        task=Task.objects.get(id=id)
        serializer=TaskSerializer
        request.data['status']='rejected'
        request.data['approvalTime']=datetime.now(tz=timezone.utc)
        serializer.Meta.fields=['approvalTime','status']
        obj=serializer(instance=task,data=request.data)
        obj.is_valid()
        obj.save()
        return Response({'message':'rejected'})


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@permissionCheckerFunc('QC')
def currentQcTask(request):
    statusQuery= r'submitted'
    tasks=Task.objects.filter(QC_id=request.user.id,status=statusQuery).order_by('-startedTime','-id')
    serializer=TaskSerializer
    serializer.Meta.fields='__all__'
    obj=serializer(data=tasks,many=True,context={'request': request})
    obj.is_valid()
    return Response(data=obj.data)