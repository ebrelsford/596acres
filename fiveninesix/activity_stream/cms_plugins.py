from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

class CMSActivityStreamPlugin(CMSPluginBase):
    name = _('Activity Stream')
    render_template = 'activity/plugin.html'

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(CMSActivityStreamPlugin)
