from django.conf.urls.defaults import patterns, url

from news.views import LanguageFallbackEntryArchiveIndexView, LanguageFallbackEntryDateDetailView, NewsletterArchiveView
from cmsplugin_blog.urls import blog_info_dict, blog_info_detail_dict

urlpatterns = patterns('',
    url(r'^newsletter/$', 
        NewsletterArchiveView.as_view(),
        name='news_newsletter_list'
    ),

    (r'^$',
        LanguageFallbackEntryArchiveIndexView.as_view(),
        blog_info_dict,
        'blog_archive_index'
    ),

    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
        LanguageFallbackEntryDateDetailView.as_view(),
        blog_info_detail_dict,
        'blog_detail'
    ),
)
