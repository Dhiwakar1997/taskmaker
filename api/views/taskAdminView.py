from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from api.models.users.models import CustomUsers
from api.models.tasks.models import Task
from api.utils.decorators import permissionChecker
from api.utils.apiFeatures import APIFeatures
from api.serializers.taskSerializer import TaskSerializer

class AdminTaskManager(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

#Remove this decorator to allow access to anyone
    @permissionChecker('admin')
    def get(self,request,format=None):
        #queryset =filter(request.query_params,Task,['designer_id','admin_id','QC_id','status'])
        queryset=APIFeatures(Task,request).filter().sort().paginate().limitFields()
        data=queryset.extract()
        return Response(data=data)

    @permissionChecker('admin')
    def post(self,request,format=None):
        request.data['admin_id']= request.user.id
        request.data['status']='assigned'
        serializer= TaskSerializer(data=request.data)
        serializer.is_valid()
        print(serializer.validated_data)
        serializer.save()
        return Response('post done')

    @permissionChecker('admin')  
    def delete(self,request,format=None):
        data=request.query_params.dict()
        data['id']=int(data['id'])
        task=Task.objects.get(id=data['id'])
        task.delete() 
        return Response({'message':'Task deleted successfully'})



def filter(userQuery,model,fields=[]):
    #fields=['designer_id','admin_id','QC_id','status']
    query={}

    for field in fields:
        if field in userQuery:
            query[field] = userQuery[field]
    if query:
        print(query)
        return model.objects.filter(**query)
    else:
        print('ALL')
        return model.objects.all()
        

