from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class LotsApphook(CMSApp):
    name = _("Lots Apphook")
    urls = ('lots.urls_app',)

apphook_pool.register(LotsApphook)

