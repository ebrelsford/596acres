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
                'organizing': Lot.objects.filter(LOT_QS['organizing']).count(),
                'accessed': Lot.objects.filter(LOT_QS['accessed']).count(),
                'private_accessed': Lot.objects.filter(LOT_QS['private_accessed']).count(),
            },
        })
        return context

plugin_pool.register_plugin(CMSLegendPlugin)
