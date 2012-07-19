from django.conf import settings
from django.http import Http404
from django.views.generic.list import ListView

from cmsplugin_blog.models import Entry
from tagging.models import TaggedItem
from tagging.utils import get_tag

class EntriesTaggedArchiveView(ListView):
    context_object_name = 'latest'
    paginate_by = 15
    template_name = 'cmsplugin_blog/entry_list.html'

    def get_context_data(self, **kwargs):
        context = super(EntriesTaggedArchiveView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag', '')
        return context

    def get_queryset(self):
        try:
            tag = self.kwargs['tag']
        except KeyError:
            raise AttributeError(_('tagged_object_list must be called with a tag.'))

        try:
            tag_instance = get_tag(tag)
            return TaggedItem.objects.get_by_model(Entry, tag_instance)
        except ValueError:
            raise Http404

class NewsletterArchiveView(ListView):
    paginate_by = 15
    template_name = 'news/newsletter_archive.html'

    def get_queryset(self):
        tag = settings.NEWSLETTER_TAG
        tag_instance = get_tag(tag)
        return TaggedItem.objects.get_by_model(Entry, tag_instance)
