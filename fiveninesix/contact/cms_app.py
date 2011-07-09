from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from contact.cms_menu import ContactMenu

class ContactApphook(CMSApp):
    name = _("Contact Apphook")
    urls = ('contact.urls',)
    menus = (ContactMenu,)

apphook_pool.register(ContactApphook)
