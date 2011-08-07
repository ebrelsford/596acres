from django.conf.urls.defaults import *

urlpatterns = patterns('contact.views',
    url(r'^join-the-team/$', 'join_us'),
    url(r'^join-the-team/thanks/$', 'join_us_thanks'),
    url(r'^lot-in-your-life/$', 'lot_info'),
    url(r'^lot-in-your-life/thanks/$', 'lot_info_thanks'),
    url(r'^contact-us/$', 'contact_us'),
    url(r'^contact-us/thanks/$', 'contact_us_thanks'),
)
