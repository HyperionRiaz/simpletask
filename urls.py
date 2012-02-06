from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^kroonm/', include('kroonm.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', 'simpletask.views.index'),
    (r'^task_list/', "simpletask.views.task_list"),
    (r'^view_task/', "simpletask.views.view_task"),
    (r'^add_task/', "simpletask.views.add_task"),
)
