from django import forms
from simpletask import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        widgets = {
            'descriptio': forms.Textarea(attrs={'cols': 35, 'rows': 10}),
        }
