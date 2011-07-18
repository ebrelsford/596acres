from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^lots/geojson', 'lots.views.lot_geojson'),
    url(r'^lot/(?P<bbl>\d+)/$', 'lots.views.details'),
    url(r'^lot/(?P<bbl>\d+)/json/$', 'lots.views.details_json'),
    url(r'^lot/(?P<bbl>\d+)/tabs/$', 'lots.views.tabs'),

    url(r'^owners/(?P<id>\d+)/details/json/$', 'lots.views.owner_details'),

    url(r'^organizers/lot/(?P<bbl>\d+)/details/json/$', 'organize.views.details'),
    url(r'^lot/(?P<bbl>\d+)/organizers/add/$', 'organize.views.add_organizer', {}, 'add_organizer'),
    url(r'^lot/(?P<bbl>\d+)/organizers/add/ajax/$', 'organize.views.add_organizer', {
        'ajax': True,
    }),
    url(r'^lot/(?P<bbl>\d+)/organizers/add/thanks/$', 'organize.views.add_organizer_thanks'),

    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns
