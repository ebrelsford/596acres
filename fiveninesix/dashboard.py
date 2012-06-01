from datetime import date, timedelta

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules, Dashboard
from admin_tools.utils import get_admin_site_name

from lots.models import Review
from organize.models import Note, Organizer, Picture, Watcher

class RecentlyAddedDashboardModule(modules.LinkList):
    def __init__(self, title='The Past 7 Days', **kwargs):
        super(RecentlyAddedDashboardModule, self).__init__(title, **kwargs)

        added_cutoff = date.today() - timedelta(days=7)
        for model in (Note, Organizer, Picture, Review, Watcher,):
            count = model.objects.filter(added__gt=added_cutoff).count()
            pluralize = 's'
            if count == 1:
                pluralize = ''

            url = reverse('admin:%s_%s_changelist' % (model.__module__.split('.')[-2], model.__name__.lower(),))

            self.children.append({
                'title': '%d %s%s' % (count, model.__name__, pluralize),
                'url': url + '?added__gte=%s' % added_cutoff.strftime('%Y-%m-%d'),
            })

class CommonTasksDashboardModule(modules.DashboardModule):
    
    def __init__(self, title='Common Tasks', **kwargs):
        super(CommonTasksDashboardModule, self).__init__(title, **kwargs)
        self.template = 'admin_tools/dashboard/common_tasks.html'
        self.children = [1,2,3]

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for fiveninesix.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(CommonTasksDashboardModule())
        self.children.append(RecentlyAddedDashboardModule())

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

