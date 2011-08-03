from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<bbl>\d+)/$', 'lots.views.details'),
    url(r'^random/$', 'lots.views.random'),
    url(r'^(?P<bbl>\d+)/organizers/add/$', 'organize.views.add_organizer', {}, 'add_organizer'),
)
