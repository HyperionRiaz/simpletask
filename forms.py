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

class ProjectForm(forms.ModelForm):

    class Meta:
        model = models.Project

class FilterForm(forms.Form):
    filter_projects = forms.ModelMultipleChoiceField(queryset=None)
    filter_task_status = forms.ModelMultipleChoiceField(queryset=models.TaskStatus.objects.all())

    def __init__(self, user, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields["filter_projects"].queryset=user.projects.all()

class ViewForm(forms.Form):
    view_class = forms.ChoiceField(choices=[("table","Table view"),
                                            ("hierarchy", "Hierarcy")
                                            ])
    verbosity = forms.ChoiceField(choices=[("min", "Minimal"),
                                            ("max", "Maximal")
                                            ])