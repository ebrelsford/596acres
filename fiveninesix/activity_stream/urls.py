from django.conf.urls.defaults import patterns, url

from activity_stream.views import LotActivityFeed, PlaceActivityFeed,\
        PlaceActivityListView

urlpatterns = patterns('',

    url(r'^feeds/all/$',
        PlaceActivityFeed(),
        name='activitystream_feed',
    ),

    url(r'^feeds/lot/(?P<bbl>\d+)/$',
        LotActivityFeed(),
        name='activitystream_feed_lot',
    ),

    url(r'^', 
        PlaceActivityListView.as_view(),
        name='activitystream_activity_list'
    ),

)
