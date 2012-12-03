from django.conf.urls.defaults import patterns, url

from activity_stream.views import PlaceActivityListView

urlpatterns = patterns('',

    url(r'^', 
        PlaceActivityListView.as_view(),
        name='activitystream_activity_list'
    ),

)
