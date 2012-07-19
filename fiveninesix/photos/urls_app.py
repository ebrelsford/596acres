from django.conf.urls.defaults import patterns, url
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView

from models import PhotoAlbum
from views import PhotoDetailView

urlpatterns = patterns('',
    url(r'^$', cache_page(60 * 60)(ListView.as_view(
            queryset=PhotoAlbum.objects.filter(parent_album=None),
        )), 
        name='photos_photoalbum_list'
    ),

    url(r'^album/(?P<pk>\d+)/$', cache_page(60 * 60)(DetailView.as_view(
            model=PhotoAlbum
        )),
        name='photos_photoalbum_detail'
    ),

    url(r'^album/(?P<album_id>\d+)/(?P<pk>\d+)/$', 
        cache_page(12 * 60 * 60)(PhotoDetailView.as_view()),
        name='photos_photo_detail'
    ),
)
