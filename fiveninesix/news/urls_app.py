from django.conf.urls.defaults import patterns, url

from news.views import NewsletterArchiveView

urlpatterns = patterns('',
    url(r'^newsletter/$', 
        NewsletterArchiveView.as_view(),
        name='news_newsletter_list'
    ),
)
