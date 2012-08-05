from django.utils import translation

def language_namespaced_view_name(view_name):
    return '%s:%s' % (translation.get_language(), view_name)
