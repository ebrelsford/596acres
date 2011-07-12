from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lots/geojson', 'lots.views.lot_geojson'),
    url(r'^lots/(?P<bbl>\d+)/details/json/$', 'lots.views.details'),
    url(r'^lot/(?P<bbl>\d+)/tabs/$', 'lots.views.tabs'),

    url(r'^owners/(?P<id>\d+)/details/json/$', 'lots.views.owner_details'),

    url(r'^organizers/lot/(?P<bbl>\d+)/details/json/$', 'organize.views.details'),

    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns
