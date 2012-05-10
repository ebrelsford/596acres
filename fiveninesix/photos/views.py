from django.views.generic import DetailView

from models import Photo

class PhotoDetailView(DetailView):
    def get_queryset(self):
        album_id = self.kwargs['album_id']
        pk = self.kwargs['pk']
        return Photo.objects.filter(album__id=album_id, pk=pk).order_by('position')
