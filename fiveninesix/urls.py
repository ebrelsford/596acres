from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^lots/geojson', 'lots.views.lot_geojson'),
    url(r'^lots/kml', 'lots.views.lot_kml'),
    url(r'^lot/(?P<bbl>\d+)/json/$', 'lots.views.details_json'),
    url(r'^lot/(?P<bbl>\d+)/tabs/$', 'lots.views.tabs'),

    url(r'^owners/(?P<id>\d+)/details/json/$', 'lots.views.owner_details'),
    url(r'^owners/json/$', 'lots.views.owners_json'),

    url(r'^organizers/lot/(?P<bbl>\d+)/details/json/$', 'organize.views.details'),
    url(r'^lot/(?P<bbl>\d+)/organizers/add/ajax/$', 'organize.views.add_organizer', {
        'ajax': True,
    }),

    url(r'^sessions/hide_map_overlay/$', 'sessions.views.hide_map_overlay'),

    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns
