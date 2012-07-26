from django.conf import settings
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView

from cmsplugin_blog.models import Entry
from cmsplugin_blog.utils import is_multilingual
from cmsplugin_blog.views import EntryDateDetailView
from menus.utils import set_language_changer
from simple_translation.middleware import filter_queryset_language
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

class LanguageFallbackEntryDateDetailView(EntryDateDetailView):
    """
    An EntryDateDetailView that falls back to the default language for 
    entries not in the current language without redirecting.
    """
    def get_object(self):
        try:
            obj = super(LanguageFallbackEntryDateDetailView, self).get_object()
        except Http404, e:
            # No entry has been found for a given language, we fallback to 
            # search for an entry in any language.
            if is_multilingual():
                try:
                    queryset = self.get_unfiltered_queryset()
                    obj = super(LanguageFallbackEntryDateDetailView, self).get_object(queryset=queryset)
                except Entry.MultipleObjectsReturned, s:
                    # Could find multiple entries, in this way we cannot decide 
                    # which one is the right one, so we let exception be 
                    # propagated.
                    raise e

                # Returning here without Redirect! This is the part that 
                # differs from EntryDateDetailView.
                return obj
            else:
                raise e

        set_language_changer(self.request, obj.language_changer)
        return obj

class LanguageFallbackEntryArchiveIndexView(ArchiveIndexView):
    """
    An EntryArchiveIndexView that falls back to the default language if there
    are no entries in the current language.

    TODO make more flexible--selectively return entries in the current 
    language, if they exist, entries in the default language otherwise.
    """
    date_field = 'pub_date'
    allow_empty = True
    paginate_by = 15
    template_name_field = 'template'
    queryset = Entry.objects.all()

    def get_dated_items(self):
        items = super(LanguageFallbackEntryArchiveIndexView, self).get_dated_items()
        from cmsplugin_blog.urls import language_changer
        set_language_changer(self.request, language_changer)
        return items

    def get_dated_queryset(self, **lookup):
        queryset = super(LanguageFallbackEntryArchiveIndexView, self).get_dated_queryset(**lookup)
        current_language_queryset = filter_queryset_language(self.request, queryset)
        if current_language_queryset.count() != 0:
            # filter with default language
            queryset = current_language_queryset
        return queryset.published()
