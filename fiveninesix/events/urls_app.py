from datetime import datetime

from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView

from models import Event

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        queryset=Event.objects.filter(status='active', start__gte=datetime.now()),
    ), name='events_event_list'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(
        model=Event,
    ), name='events_event_detail'),
)
