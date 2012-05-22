from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^lots/geojson', 'lots.views.lot_geojson'),
    url(r'^lots/kml', 'lots.views.lot_kml'),
    url(r'^lots/csv', 'lots.views.lot_csv'),
    url(r'^lots/(?P<bbl>\d+)/review/$', 'lots.views.add_review'),
    url(r'^lot/(?P<bbl>\d+)/json/$', 'lots.views.details_json'),
    url(r'^lot/(?P<bbl>\d+)/tabs/$', 'lots.views.tabs'),

    url(r'^owners/(?P<id>\d+)/details/json/$', 'lots.views.owner_details'),
    url(r'^owners/json/$', 'lots.views.owners_json'),

    url(r'^organizers/lot/(?P<bbl>\d+)/details/json/$', 'organize.views.details'),
    url(r'^lot/(?P<bbl>\d+)/organizers/add/ajax/$', 'organize.views.add_organizer', {
        'ajax': True,
    }),

    url(r'^watchers/(?P<hash>[^/]{9,})/$', 'organize.views.edit_watcher'),
    url(r'^watchers/(?P<hash>[^/]{9,})/delete/(?P<id>\d+)/$', 'organize.views.delete_watcher'),

    url(r'^sessions/hide_map_overlay/$', 'sessions.views.hide_map_overlay'),

    # auth
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/password/change/$', 'django.contrib.auth.views.password_change'),
    (r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done'),
    (r'^accounts/password/reset/$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/email=(?P<email>.*)$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^accounts/password/reset/confirm?uid=(?P<uidb36>.*)&token=(?P<token>.*)$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),

    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns
