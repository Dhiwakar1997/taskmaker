from django.contrib import admin
from api.models.users.models import CustomUsers
from api.models.tasks.models import Task
# Register your models here.
admin.site.register(CustomUsers)
admin.site.register(Task)