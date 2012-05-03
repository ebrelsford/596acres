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
            NavigationNode(_('Come to an Upcoming Event'),
                           reverse('events_event_list'), 3),
            NavigationNode(_('Work With Us'),
                           reverse('blog_archive_tagged', 
                                   kwargs={ 'tag': 'opportunities'}), 4),
        ]
        return nodes

menu_pool.register_menu(GetInvolvedMenu)
