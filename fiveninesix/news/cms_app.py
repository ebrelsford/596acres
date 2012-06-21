from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class NewsApphook(CMSApp):
    name = _("News Apphook")
    urls = ('news.urls_app', 'cmsplugin_blog.urls',)

apphook_pool.register(NewsApphook)
