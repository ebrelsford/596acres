from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^(?P<bbl>\d+)/$', 'lots.views.details', name='lots_lot_details'),
)
