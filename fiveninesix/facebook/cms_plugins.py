from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import FacebookPhotoPlugin, FacebookLikeboxPlugin

class CMSFacebookPhotoPlugin(CMSPluginBase):
    model = FacebookPhotoPlugin
    name = _('Facebook Photos')
    render_template = 'facebook/photo.html'

    def render(self, context, instance, placeholder):
        context.update({
            'account': instance.account,
            'width': instance.width,
            'object': instance,
            'placeholder': placeholder,
        })
        return context

class CMSFacebookLikeboxPlugin(CMSPluginBase):
    model = FacebookLikeboxPlugin
    name = _('Facebook Likebox')
    render_template = 'facebook/likebox.html'

    def render(self, context, instance, placeholder):
        context.update({
            'page': instance.page,
            'object': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(CMSFacebookPhotoPlugin)
plugin_pool.register_plugin(CMSFacebookLikeboxPlugin)
