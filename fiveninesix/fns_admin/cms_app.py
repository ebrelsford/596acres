from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class FNSAdminApphook(CMSApp):
    name = _("596 Admin Apphook")
    urls = ('fns_admin.urls_app',)

apphook_pool.register(FNSAdminApphook)
