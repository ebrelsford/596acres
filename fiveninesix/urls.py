from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from news.views import EntriesTaggedArchiveView
from organize.models import Organizer, Watcher
from organize.views import DeleteParticipantView
from sizecompare import urls as sizecompare_urls

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
    url(r'^oasis_popup/', 'lots.views.oasis_popup'),

    url(r'^owners/(?P<id>\d+)/details/json/$', 'lots.views.owner_details'),
    url(r'^owners/json/$', 'lots.views.owners_json'),

    url(r'^organizers/lot/(?P<bbl>\d+)/details/json/$', 'organize.views.details'),
    url(r'^lot/(?P<bbl>\d+)/organizers/add/ajax/$', 'organize.views.add_organizer', {
        'ajax': True,
    }),

    url(r'^watchers/(?P<hash>[^/]{9,})/$', 'organize.views.edit_participant'),
    url(r'^user-accounts/(?P<hash>[^/]{9,})/$', 'organize.views.edit_participant'),

    url(r'^organizers/delete/(?P<pk>\d+)/$', 
        DeleteParticipantView.as_view(
            model=Organizer,
        ),
        name='organize_organizer_delete',
    ),

    url(r'^watchers/delete/(?P<pk>\d+)/$', 
        DeleteParticipantView.as_view(
            model=Watcher,
        ),
        name='organize_watcher_delete',
    ),

    url(r'^size-compare/', include(sizecompare_urls)),
    url(r'^sessions/hide_map_overlay/$', 'sessions.views.hide_map_overlay'),

    # TODO extend BlogApphook, point to paginated views by default?
    url(r'^news/tag/(?P<tag>[^/]+)/$', 
        EntriesTaggedArchiveView.as_view(),
        name='blog_archive_tagged_paginated'
    ),

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

    ('^activity/', include('actstream.urls')),

    (r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
