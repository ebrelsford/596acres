from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

class GetInvolvedMenu(CMSAttachMenu):
    name = _("get involved menu")

    def get_nodes(self, request):
        nodes = [
            NavigationNode(_('Come to an Upcoming Event'),
                           reverse('en:events_event_list'), 3),
            NavigationNode(_('Work With Us'),
                           reverse('blog_archive_tagged_paginated',
                                   kwargs={ 'tag': 'opportunities'}), 4),
        ]
        return nodes

menu_pool.register_menu(GetInvolvedMenu)
