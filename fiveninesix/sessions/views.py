import json

from django.http import HttpResponse

def hide_map_overlay(request):
    request.session['hide_map_overlay'] = True
    return HttpResponse(json.dumps({ 'success': True }), mimetype='application/json')
