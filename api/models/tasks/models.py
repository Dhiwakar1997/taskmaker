from django.db import models

# Create your models here.
class Task(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)
    description=models.CharField(max_length=300,blank=True,null=True)
    workFiles=models.FileField(upload_to='taskAssained/',blank=True,null=True)
    submittedFiles=models.FileField(upload_to='taskSubmitted/',blank=True,null=True)

    STATUS=(
        ('assigned','Work assigned not started'),
        ('started','Word started'),
        ('submitted','Work submitted for Quality Check'),
        ('completed','Work completed and approved'),
        ('rejected','Work rejected'))
    status=models.CharField(max_length=20,choices=STATUS,blank=True,null=True)

    admin_id=models.IntegerField(blank=True, null=True)
    QC_id=models.IntegerField(blank=True, null=True)
    designer_id=models.IntegerField(blank=True, null=True)
    assignedTime=models.DateTimeField(auto_now_add=True)
    startedTime=models.DateTimeField(blank=True, null=True)
    submittedTime=models.DateTimeField(blank=True, null=True)
    approvalTime=models.DateTimeField(blank=True, null=True)