from django.conf import settings
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_blog.models import Entry
from tagging.models import TaggedItem
from tagging.utils import get_tag

class RecentNewsletterExcerptPlugin(CMSPluginBase):
    name = _('Recent Newsletter Excerpt')
    render_template = 'news/recent_excerpt.html'

    def render(self, context, instance, placeholder):
        tag_instance = get_tag(settings.NEWSLETTER_TAG)
        entry = TaggedItem.objects.get_by_model(Entry, tag_instance).order_by('-pub_date')[0]
        context.update({
            'entry': entry,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(RecentNewsletterExcerptPlugin)
