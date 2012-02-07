from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=200)
    manager = models.ForeignKey("auth.User", related_name = "pm_projects")
    deputy_manager = models.ForeignKey("auth.User", related_name = "dm_projects")
    group = models.ManyToManyField("auth.Group", related_name = "projects")
    maindoc = models.ForeignKey("DocPage", related_name="++")


    def __unicode__(self):
        return self.name

    def html_diagram(self):
        '''This Function generates a diagram that shows all the tasks in a project'''
        grid=[[0]]
        docpages = self.get_docpages()
        return r"<p>not working yet</p>"

    def get_docpages(self):
        q1 = models.Q(used_by__project=self)
        q2 = models.Q(produced_by__project=self)
        return DocPage.objects.filter(q1 | q2).all()
        
class DocPage(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __unicode__(self):
        return self.title

class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks")
    title = models.CharField(max_length=200)
    descriptio = models.CharField(max_length=2000)
    creator = models.ForeignKey("auth.User", related_name="tasks_created")
    owners = models.ManyToManyField("auth.User", related_name="tasks_owned")
    deadline = models.DateField()
    priority = models.IntegerField(choices=((1,"Emergency"),
            (2,"Very urgent"),
            (3,"Urgent"),
            (4,"Normal"),
            (5,"Maybe"),
            )
        )
    status = models.CharField(max_length=20)
    inputs = models.ManyToManyField(DocPage, related_name = "used_by", blank=True, null=True)
    outputs = models.ManyToManyField(DocPage, related_name = "produced_by", blank=True, null=True)

    def __unicode__(self):
        return self.title
