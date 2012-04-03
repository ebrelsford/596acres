from datetime import datetime

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from events.models import Event, UpcomingEventsPlugin

class CMSUpcomingEventsPlugin(CMSPluginBase):
    model = UpcomingEventsPlugin
    name = _('Upcoming Events')
    render_template = 'events/upcoming_events_plugin.html'

    def render(self, context, instance, placeholder):
        events = Event.objects.filter(status='active', start__gte=datetime.now()).order_by('start')[:instance.max_events]
        context.update({
            'object': instance,
            'placeholder': placeholder,
            'events': events,
        })
        return context

plugin_pool.register_plugin(CMSUpcomingEventsPlugin)
