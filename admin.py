from django.contrib import admin 
from simpletask.models import Task, Project, Tags, TaskStatus

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Tags)
admin.site.register(TaskStatus)
