from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

class CMSLegendPlugin(CMSPluginBase):
    name = _('Map Legend')
    render_template = 'legend/legend.html'

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context

class CMSSandyLegendPlugin(CMSPluginBase):
    name = _('Sandy Map Legend')
    render_template = 'legend/sandy_legend.html'

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(CMSLegendPlugin)
plugin_pool.register_plugin(CMSSandyLegendPlugin)
