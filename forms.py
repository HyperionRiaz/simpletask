from django import forms
from django.forms import HiddenInput
from simpletask import models

class TaskForm(forms.ModelForm):

    class Meta:
        model = models.Task
        widgets = {
            "opened_by": HiddenInput()
            }
        exclude = ("last_edited", "created_date")

