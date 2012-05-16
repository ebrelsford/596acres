from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

class AboutMenu(CMSAttachMenu):
    name = _("about menu")

    def get_nodes(self, request):
        nodes = [
            NavigationNode(_('Previous Events'),
                           reverse('events_event_list_past'), 1),
            NavigationNode(_('Acres in Pictures'),
                           reverse('photos_photoalbum_list'), 2),
        ]
        return nodes

menu_pool.register_menu(AboutMenu)
