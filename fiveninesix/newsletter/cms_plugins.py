from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import MailchimpPlugin

class CMSMailchimpPlugin(CMSPluginBase):
    model = MailchimpPlugin
    name = _('Mailchimp Signup')
    render_template = 'newsletter/mailchimp_signup.html'

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(CMSMailchimpPlugin)
