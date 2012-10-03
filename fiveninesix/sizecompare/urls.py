from django.conf.urls.defaults import patterns, url

from sizecompare.views import FindComparableView

urlpatterns = patterns('',
    url(r'^find',
        FindComparableView.as_view(),
        name='sizecompare_find_comparable'),
)
