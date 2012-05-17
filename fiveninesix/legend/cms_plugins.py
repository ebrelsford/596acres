from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from lots.models import LOT_QUERIES

class CMSLegendPlugin(CMSPluginBase):
    name = _('Map Legend')
    render_template = 'legend/legend.html'

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
            'counts': {
                'vacant': LOT_QUERIES['vacant'].count(),
                'organizing': LOT_QUERIES['organizing'].count(),
                'accessed': LOT_QUERIES['accessed'].count(),
                'garden': LOT_QUERIES['garden'].count(),
                'private': LOT_QUERIES['private'].count(),
                'inaccessible': LOT_QUERIES['inaccessible'].count(),
                'gutterspace': LOT_QUERIES['gutterspace'].count(),
            },
        })
        return context

plugin_pool.register_plugin(CMSLegendPlugin)
