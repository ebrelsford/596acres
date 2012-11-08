from django.conf.urls.defaults import *

from organize.models import Organizer, Watcher
from organize.views import AddParticipantSuccessView

urlpatterns = patterns('',
    url(r'^(?P<bbl>\d+)/$', 'lots.views.details', name='lots_lot_details'),
    url(r'^(?P<bbl>\d+)/pdf/$', 'lots.views.pdf'),
    url(r'^(?P<bbl>\d+)/qrcode/$', 'lots.views.qrcode'),
    url(r'^random/$', 'lots.views.random'),

    url(r'^(?P<bbl>\d+)/organizers/add/$', 'organize.views.add_organizer', {}, 'add_organizer'),
    url(r'^(?P<bbl>\d+)/organizers/add-success/(?P<email_hash>[^/]+)/$',
        AddParticipantSuccessView.as_view(
            model=Organizer,
            template_name='organize/add_organizer_success.html',
        ),
        name='organize_organizer_add_success'
    ),

    url(r'^(?P<bbl>\d+)/watchers/add/$', 'organize.views.add_watcher'),
    url(r'^(?P<bbl>\d+)/watchers/add-success/(?P<email_hash>[^/]+)/$',
        AddParticipantSuccessView.as_view(
            model=Watcher,
            template_name='organize/add_watcher_success.html',
        ),
        name='organize_watcher_add_success'
    ),

    url(r'^(?P<bbl>\d+)/notes/add/$', 'organize.views.add_note'),
    url(r'^(?P<bbl>\d+)/pictures/add/$', 'organize.views.add_picture'),
    url(r'^(?P<bbl>\d+)/organizers/(?P<id>\d+)/edit/$', 'organize.views.edit_organizer'),
    url(r'^counts$', 'lots.views.counts'),
)
