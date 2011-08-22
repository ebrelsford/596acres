from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

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

