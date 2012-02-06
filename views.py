from django.http import HttpResponse
from django.template import Context, loader
from simpletask.models import Task, Project, DocPage
from simpletask.forms import TaskForm

framename = "cs_website/index.html"
blockname = "maincontent"

default_context = Context({"framename":framename, "blockname":blockname})
# Create your views here.

def index(request):
    c=Context({})
    c.update(default_context)
    user = request.user
    projects = Project.objects.filter(group__in=user.groups.all())
    c["projects"]=projects
    t = loader.get_template("simpletask/index.html")
    return HttpResponse(t.render(c))

def task_list(request):
    return HttpResponse("This is the task_list")

def view_task(request):
    return HttpResponse("This is a single task")

def add_task(request):
    template = loader("simpletask/task/add.html")
    context = default_context.copy()
    form = TaskForm()

    return HttpResponse("Here you can add a task")


