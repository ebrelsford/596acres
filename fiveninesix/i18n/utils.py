from django.conf import settings
from django.utils import translation

def language_namespaced_view_name(view_name, lang=None):
    if not lang:
        try:
            lang = translation.get_language().split('-')[0]
        except Exception:
            pass
    if not lang:
        lang = settings.LANGUAGE_CODE
    return '%s:%s' % (lang, view_name)
