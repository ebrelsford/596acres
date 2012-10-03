from json import dumps

from django.http import HttpResponse
from django.views.generic import View

from sizecompare.util import find_comparable

class FindComparableView(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(mimetype='application/json')
        response.write(dumps(
            find_comparable(**{
                'acres': request.GET.get('acres', None),
                'sqft': request.GET.get('sqft', None),
            })
        ))
        return response
