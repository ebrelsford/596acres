from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

class GetInvolvedMenu(CMSAttachMenu):
    name = _("get involved menu")

    def get_nodes(self, request):
        nodes = [
            NavigationNode(_('Contact Us'), 
                           reverse('contact.views.contact_us'), 1),
            NavigationNode(_('Tell Us About the Lot in Your Life'),
                           reverse('contact.views.lot_info'), 2),
            NavigationNode(_('Upcoming Events'),
                           reverse('events_event_list'), 3),
        ]
        return nodes

menu_pool.register_menu(GetInvolvedMenu)
