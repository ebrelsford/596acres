from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from lots.models import Lot, LOT_QS

class CMSLegendPlugin(CMSPluginBase):
    name = _('Map Legend')
    render_template = 'legend/legend.html'

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
            'counts': {
                'organizing_sites': Lot.objects.filter(LOT_QS['organizing_sites']).count(),
                'accessed_sites': Lot.objects.filter(LOT_QS['accessed_sites']).count(),
                'private_accessed_sites': Lot.objects.filter(LOT_QS['private_accessed_sites']).count(),
            },
        })
        return context

plugin_pool.register_plugin(CMSLegendPlugin)
