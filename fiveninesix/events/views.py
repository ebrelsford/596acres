from datetime import datetime

from django.views.generic import ListView

from models import Event

class EventListView(ListView):
    queryset = Event.objects.filter(status='active').order_by('start')

    def get_queryset(self):
        self.past = self.kwargs.get('past', False)
        if self.past:
            return self.queryset.filter(start__lt=datetime.now())
        else:
            return self.queryset.filter(start__gte=datetime.now())

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        context['past'] = self.past
        return context
