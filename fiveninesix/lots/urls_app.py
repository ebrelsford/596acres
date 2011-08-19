from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<bbl>\d+)/$', 'lots.views.details'),
    url(r'^random/$', 'lots.views.random'),
    url(r'^(?P<bbl>\d+)/organizers/add/$', 'organize.views.add_organizer', {}, 'add_organizer'),
    url(r'^(?P<bbl>\d+)/organizers/(?P<id>\d+)/edit/$', 'organize.views.edit_organizer'),
    url(r'^(?P<bbl>\d+)/organizers/(?P<id>\d+)/delete/$', 'organize.views.delete_organizer'),
)
