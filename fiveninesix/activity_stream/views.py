from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.feeds import GeoFeedMixin, GeoRSSFeed
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from actstream.models import Action

from lots.models import Lot

class PlaceActivityListView(ListView):
    model = Action
    paginate_by = 5
    template_name = 'activity/action_list.html'

    def get_queryset(self):
        qs = self.model.objects.public()
        filters = self.request.GET

        try:
            qs = self.model.objects.in_bbox(filters['bbox'].split(','))
        except Exception:
            pass
        return qs

class PlaceActivityFeed(Feed, GeoFeedMixin):
    feed_type = GeoRSSFeed
    subtitle = 'Recent activity at 596 Acres'
    title = '596 Acres activity stream'

    def items(self):
        return Action.objects.all().order_by('-timestamp')[:10]

    def item_extra_kwargs(self, item):
        return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.place

    def link(self):
        return reverse('activitystream_feed')

class LotActivityFeed(PlaceActivityFeed):

    def get_object(self, request, *args, **kwargs):
        return get_object_or_404(Lot, bbl=kwargs.get('bbl', None))

    def items(self, obj):
        return Action.objects.filter(
            target_object_id=obj.pk,
            target_content_type=ContentType.objects.get_for_model(obj),
        ).order_by('-timestamp')[:10]

    def link(self, obj):
        return reverse('activitystream_feed_lot', kwargs={ 'bbl': obj.bbl })

    def subtitle(self, obj):
        return 'Recent activity on ' + obj.display_name

    def title(self, obj):
        return '596 Acres: Recent activity on ' + obj.display_name

# TODO feed for user/bbox
