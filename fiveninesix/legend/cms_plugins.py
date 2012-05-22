from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from lots.models import LOT_QUERIES

class CMSLegendPlugin(CMSPluginBase):
    name = _('Map Legend')
    render_template = 'legend/legend.html'

    # TODO don't be hard-coded for Brooklyn

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
            'counts': {
                'vacant': LOT_QUERIES['vacant'].filter(borough='Brooklyn').count(),
                'organizing': LOT_QUERIES['organizing'].filter(borough='Brooklyn').count(),
                'accessed': LOT_QUERIES['accessed'].filter(borough='Brooklyn').count(),
                'garden': LOT_QUERIES['garden'].filter(borough='Brooklyn').count(),
                'private_accessed': LOT_QUERIES['private_accessed'].filter(borough='Brooklyn').count(),
                'inaccessible': LOT_QUERIES['inaccessible'].filter(borough='Brooklyn').count(),
                'gutterspace': LOT_QUERIES['gutterspace'].filter(borough='Brooklyn').count(),
            },
        })
        return context

plugin_pool.register_plugin(CMSLegendPlugin)
