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
        nodes.append(NavigationNode(_('Events'), self._get_tag_url('events'), 1))
        nodes.append(NavigationNode(_('Press'), self._get_tag_url('press'), 2))
        return nodes

menu_pool.register_menu(NewsMenu)

