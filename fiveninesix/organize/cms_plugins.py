from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from lots.models import Lot

class CMSOrganizingTallyPlugin(CMSPluginBase):
    name = _('Organizing Tally')
    render_template = 'organize/tally.html'

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
            'organizing_count': Lot.objects.filter(is_vacant=True).exclude(organizer=None).count(),
        })
        return context

plugin_pool.register_plugin(CMSOrganizingTallyPlugin)
