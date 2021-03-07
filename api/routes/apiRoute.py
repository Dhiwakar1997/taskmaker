from django.urls import path,include

urlpatterns=[
path('user/',include('api.routes.userRoute'),name="user"),
path('task/',include('api.routes.taskRoute'),name="task")
]