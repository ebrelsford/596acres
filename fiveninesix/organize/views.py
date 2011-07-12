import json

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from lots.models import Lot
from forms import OrganizerForm
from models import Organizer, OrganizerType

def details(request, bbl=None):
    organizers = Organizer.objects.filter(lots__bbl=bbl)

    details = []
    for organizer in organizers:
        details.append({
            'name': organizer.name,
            'phone': organizer.phone,
            'email': organizer.email,
            'url': organizer.url,
            'type': organizer.type.name,
            'lots': [l.bbl for l in organizer.lots.all()]
        })
    return HttpResponse(json.dumps(details), mimetype='application/json')

def add_organizer(request, bbl=None):
    if request.method == 'POST':    
        form = OrganizerForm(request.POST)
        if form.is_valid():
            organizer = form.save()
            #return redirect(add_organizer_thanks)
            return add_organizer_thanks(request)
    else:
        form = OrganizerForm(initial={
            'lots': Lot.objects.filter(bbl=bbl)
        })

    return render_to_response('organize/add_organizer.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def add_organizer_thanks(request):
    return render_to_response('organize/add_organizer_thanks.html', {}, context_instance=RequestContext(request))
