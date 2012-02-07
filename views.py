from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from simpletask.models import Task, Project, DocPage
from simpletask.forms import TaskForm
from django.core.context_processors import csrf

framename = "cs_website/index.html"
blockname = "maincontent"

default_context = Context({"framename":framename, "blockname":blockname})
# Create your views here.

def index(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect("/auth/login")
    c=Context({})
    c.update(default_context)
    user = request.user
    projects = Project.objects.filter(group__in=user.groups.all()).distinct()
    c["projects"]=projects
    t = loader.get_template("simpletask/index.html")
    return HttpResponse(t.render(c))

def updatetaskdiv(request):
    taskid=request.GET["taskid"]
    t=loader.get_template("simpletask/tasks/updatetaskdiv.html")
    c=RequestContext(request)
    if taskid!="new":
        task = Task.objects.get(pk=taskid)
        form=TaskForm(instance=task)
    else:
        form = TaskForm()
    c["taskid"]=taskid
    c["form"]=form
    return HttpResponse(t.render(c))

def edit_task(request):
    taskid=request.POST["taskid"]
    if taskid!="new":
        task=Task.objects.get(pk=taskid)
        form=TaskForm(request.POST, instance=task)
    else:
        form=TaskForm(request.POST)
    form.save()
    return HttpResponseRedirect("/simpletask/")

def task_list(request):
    return HttpResponse("This is the task_list")

def view_task(request):
    return HttpResponse("This is a single task")

def add_task(request):
    template = loader("simpletask/task/add.html")
    context = default_context.copy()
    form = TaskForm()

    return HttpResponse("Here you can add a task")


