from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

class NewsMenu(CMSAttachMenu):
    name = _("news menu")

    def get_nodes(self, request):
        nodes = []
        nodes.append(NavigationNode(_('Announcements'), _get_tag_url('announcements'), 1))
        nodes.append(NavigationNode(_('Events'), _get_tag_url('events'), 2))
        nodes.append(NavigationNode(_('Press'), _get_tag_url('press'), 3))
        return nodes

    def _get_tag_url(tag):
        return reverse('blog_archive_tagged', kwargs={ 'tag': tag })

menu_pool.register_menu(NewsMenu)

