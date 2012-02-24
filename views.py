from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from simpletask.models import Task, Project
from simpletask.forms import TaskForm
from django.contrib.auth.decorators import login_required
import datetime


# Create your views here.

def index(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect("/auth/login")
    try:
        notice = request.REQUEST["notice"]
    except:
        notice=False
    c=Context({})
    user = request.user
    projects = user.projects.all()
    c["projects"]=projects
    c["notice"]=notice
    t = loader.get_template("simpletask/views/user_table.html")
    return HttpResponse(t.render(c))

def task_list(request):
    return HttpResponse("This is the task_list")

def view_task(request):
    return HttpResponse("This is a single task")

def new_task(request):
    if request.method == 'POST': # If the form has been submitted...
        form = TaskForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/simpletask")
    elif request.method == "GET":
        initial_data = {}
        try:
            project_pk = request.GET["project"]
            p = Project.objects.get(pk=project_pk)
            initial_data["project"] = project_pk
            initial_data["members"] = p.members.values_list("pk", flat=True)
        except:
            pass
        try:
            parent_id = request.GET["parent"]
            initial_data["parents"] = [parent_id]
        except:
            pass
        initial_data["assigned_to"]=request.user.pk
        initial_data["opened_by"]=request.user.pk
        form = TaskForm(initial=initial_data) # An unbound form
    else:
        form = TaskForm()
    t=loader.get_template('simpletask/tasks/new_task.html')
    c = RequestContext(request)
    c['form'] = form
    return HttpResponse(t.render(c))

def edit_task(request):
    if request.method == 'POST':
        task = Task.objects.get(pk=request.POST["pk"])
        form=TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/simpletask")
    else:
        task = Task.objects.get(pk=request.GET["pk"])
        form=TaskForm(instance=task)

    t=loader.get_template("simpletask/tasks/edit_task_div.html")
    c=RequestContext(request)
    c["form"]=form
    c["task"]=task

    return HttpResponse(t.render(c))

def delete_task(request):
    task = Task.objects.get(pk=request.GET["pk"])
    task.delete()
    return HttpResponse('Deleted')
    
@login_required
def hierarchy(request):
    projects = request.user.projects.all()
    t = loader.get_template("simpletask/views/user_hierarchy.html")
    c = Context({"projects":projects})
    return HttpResponse(t.render(c))


