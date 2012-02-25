from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from simpletask.models import Task, Project
from simpletask.forms import TaskForm, FilterForm, ViewForm
from django.contrib.auth.decorators import login_required
import datetime

# Declare global variables

viewtemplates = {
    "table":"simpletask/views/user_table.html",
    "hierarchy":"simpletask/views/user_hierarchy.html"
    }

# Create your views here.

@login_required
def index(request):
    c=RequestContext(request)
    user = request.user
    projects = user.projects.all()
    c["projects"]=projects
    c["filterform"] = FilterForm(request.user)
    c["viewform"] = ViewForm()
    
    t = loader.get_template("simpletask/simpletask_frame.html")
    return HttpResponse(t.render(c))

@login_required
def task_list(request):
    return HttpResponse("This is the task_list")

@login_required
def view_task(request):
    return HttpResponse("This is a single task")

@login_required
def new_task(request):
    if request.method == 'POST': # If the form has been submitted...
        form = TaskForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form.save()
            return HttpResponse("Task saved")
        
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

@login_required
def edit_task(request):
    if request.method == 'POST':
        task = Task.objects.get(pk=request.POST["pk"])
        form=TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponse("Changes saved")
    else:
        task = Task.objects.get(pk=request.GET["pk"])
        form=TaskForm(instance=task)

    t=loader.get_template("simpletask/tasks/edit_task_div.html")
    c=RequestContext(request)
    c["form"]=form
    c["task"]=task

    return HttpResponse(t.render(c))

@login_required
def delete_task(request):
    task = Task.objects.get(pk=request.GET["pk"])
    task.delete()
    return HttpResponse('Deleted')
    
@login_required
def hierarchy(request):
    projects = request.user.projects.all()
    t = loader.get_template("simpletask/views/user_hierarchy.html")
    c["filterform"] = FilterForm(request.user)
    c["viewform"] = ViewForm()
    c = RequestContext(request,{"projects":projects})
    return HttpResponse(t.render(c))

@login_required
def display_window(request):
    #This page must get POST data
    if request.method != "POST":
        c=RequestContext(request)
        user = request.user
        projects = user.projects.all()
        c["projects"]=projects
        c["filterform"] = FilterForm(request.user)
        c["viewform"] = ViewForm()
        t = loader.get_template("simpletask/simpletask_frame.html")
        return HttpResponse(t.render(c))
    else:
        #Get arguments
        filterform = FilterForm(request.user, request.POST)
        if filterform.is_valid():
            filter_args = filterform.cleaned_data
        viewform = ViewForm(request.POST)
        if viewform.is_valid():
            view_args = viewform.cleaned_data

        #Get data to be displayed
        c=RequestContext(request)
        t=loader.get_template(viewtemplates[view_args["view_class"]])
        c["projects"] = filter_args["filter_projects"]
        
        return HttpResponse(t.render(c))
        