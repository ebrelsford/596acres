from datetime import datetime

from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView

from models import Event

# TODO month view https://github.com/justinlilly/django-gencal or https://github.com/visualspace/django-agenda ?
urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        queryset=Event.objects.filter(status='active', start__gte=datetime.now()).order_by('start'),
    ), name='events_event_list'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(
        model=Event,
    ), name='events_event_detail'),
)
