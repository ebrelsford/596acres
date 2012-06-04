from django.conf import settings

def mobile(request):
    """
    Add is_mobile: True if user agent contains an obvious smartphone, False otherwise
    """
    try:
        ua = request.META['HTTP_USER_AGENT'].lower()
    except KeyError:
        ua = ''
    return { 'is_mobile': 'iphone' in ua or 'android' in ua, }

def public_boroughs(request):
    return {
        'public_boroughs': settings.PUBLIC_BOROUGHS,
    }
