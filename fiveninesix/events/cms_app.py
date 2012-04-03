from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class EventsApphook(CMSApp):
    name = _("Events Apphook")
    urls = ('events.urls_app',)

apphook_pool.register(EventsApphook)
