from django.db import models
from django.template import Context, loader

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=20)
    manager = models.ForeignKey("auth.User", related_name = "pm_projects")
    deputy_manager = models.ForeignKey("auth.User", related_name = "dpm_projects")
    client = models.ManyToManyField("auth.Group", related_name = "projects")
    wikipage = models.URLField()
    members = models.ManyToManyField("auth.User", related_name = "projects")
    client_contact = models.ForeignKey("auth.User", related_name ="project_contact_projects")
    last_edited = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def root_tasks(self):
        return self.tasks.filter(parents__isnull=True).all()
        
    def hierarchy_div(self):
        print "Project:", self.name
        t = loader.get_template("simpletask/projects/project_hierarchy.html")
        c = Context({"project":self})
        return t.render(c)

#######################################
#From previous version    def html_diagram(self):
#        '''This Function generates a diagram that shows all the tasks in a project'''
#        grid=[[0]]
#        docpages = self.get_docpages()
#        return r"<p>not working yet</p>"#
#
#    def get_docpages(self):
#        q1 = models.Q(used_by__project=self)
#        q2 = models.Q(produced_by__project=self)
#        return DocPage.objects.filter(q1 | q2).all()
#        
#class DocPage(models.Model):
#    title = models.CharField(max_length=200)
#    text = models.TextField()#
#
#    def __unicode__(self):
#        return self.title
#
#######################################
class Tags(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __unicode__(self):
        return self.name
        
class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks")
    name = models.CharField(max_length=20)
    notes = models.TextField(null=True)
    opened_by = models.ForeignKey("auth.User", related_name = "tasks_created")
    members = models.ManyToManyField("auth.User", related_name = "all_task")
    assigned_to = models.ForeignKey("auth.User", related_name = "assigned_tasks")
    deadline = models.DateField()
    priority = models.IntegerField()
    estimated_time = models.DecimalField(max_digits=15, decimal_places=2)
    actual_time = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    tags = models.ManyToManyField(Tags, related_name="tasks", blank=True)
    status = models.CharField(max_length=20)
    children = models.ManyToManyField("self", symmetrical=False, related_name = "parents", blank=True)
    last_edited = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    wikipage = models.URLField()
    repetition_score = models.IntegerField()

    def __unicode__(self):
            return self.name

    def hierarchy_div(self):
        print "Task hierarchy", self.name
        print "children:", self.children.all()
        t = loader.get_template("simpletask/tasks/task_hierarchy.html")
        c = Context({"task":self})
        return t.render(c)