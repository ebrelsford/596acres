from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView

from models import Event
from views import EventListView

# TODO month view https://github.com/justinlilly/django-gencal or https://github.com/visualspace/django-agenda ?
urlpatterns = patterns('',
    url(r'^$', EventListView.as_view(), name='events_event_list'),
    url(r'^past/$', EventListView.as_view(), kwargs={'past': True}, name='events_event_list_past'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(
        model=Event,
    ), name='events_event_detail'),
)
