from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

class NewsMenu(CMSAttachMenu):
    name = _("news menu")

    def _get_tag_url(self, tag):
        return reverse('blog_archive_tagged_paginated', kwargs={ 'tag': tag })

    def get_nodes(self, request):
        nodes = []
        nodes.append(NavigationNode(_('New Tools'), self._get_tag_url('tool updates'), 1))
        nodes.append(NavigationNode(_('Announcements'), self._get_tag_url('announcements'), 2))
        nodes.append(NavigationNode(_('News from the Acres'),
                                    reverse('en:news_newsletter_list'), 2))
        nodes.append(NavigationNode(_('Archive'), reverse('en:blog_archive_index'), 2))
        return nodes

menu_pool.register_menu(NewsMenu)
