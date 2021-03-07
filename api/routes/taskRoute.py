from django.urls import path,include
from api.views.taskAdminView import AdminTaskManager
from api.views.taskQcView import QcTaskManager,currentQcTask
from api.views.taskDesignerView import DesignerTaskManager,currentDesignerTask

urlpatterns = [
    path('admin/',AdminTaskManager.as_view(),name="adminView"),
    path('QC/',currentQcTask,name="QcDetailView"),
    path('QC/<int:id>/',QcTaskManager.as_view(),name="QcView"),
    path('designer/',currentDesignerTask,name="designerDetailView"),
    path('designer/<int:id>/',DesignerTaskManager.as_view(),name="designerView"),

]