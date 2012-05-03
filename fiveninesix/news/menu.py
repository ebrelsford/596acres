from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

class NewsMenu(CMSAttachMenu):
    name = _("news menu")

    def _get_tag_url(self, tag):
        return reverse('blog_archive_tagged', kwargs={ 'tag': tag })

    def get_nodes(self, request):
        nodes = []
        nodes.append(NavigationNode(_('Announcements'), self._get_tag_url('announcements'), 2))
        nodes.append(NavigationNode(_('596 Acres Press'), self._get_tag_url('596 acres press'), 2))
        nodes.append(NavigationNode(_('Of note'), self._get_tag_url('of note'), 1))
        nodes.append(NavigationNode(_('Site Updates'), self._get_tag_url('site updates'), 1))
        return nodes

menu_pool.register_menu(NewsMenu)

