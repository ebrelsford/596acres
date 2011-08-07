from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu

class ContactMenu(CMSAttachMenu):
    name = _("contact menu")

    def get_nodes(self, request):
        nodes = []
        nodes.append(NavigationNode(_('Tell Us About the Lot in Your Life'), '/get-involved/lot-in-your-life/', 1))
        nodes.append(NavigationNode(_('Join The 596 Acres Distribution Team'), '/get-involved/join-the-team/', 2))
        nodes.append(NavigationNode(_('Contact Us'), '/get-involved/contact-us/', 3))
        return nodes

menu_pool.register_menu(ContactMenu)
