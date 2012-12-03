from django.views.generic import ListView

from actstream.models import Action

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
