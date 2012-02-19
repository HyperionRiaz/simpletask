from django import forms
from simpletask import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task

