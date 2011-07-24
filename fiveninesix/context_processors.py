def mobile(request):
    """
    Add is_mobile: True if user agent contains an obvious smartphone, False otherwise
    """
    ua = request.META['HTTP_USER_AGENT'].lower()
    return { 'is_mobile': 'iphone' in ua or 'android' in ua, }
