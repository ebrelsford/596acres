import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
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

def details_tab(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)

    return render_to_response('organize/tab.html', {
        'organizers': lot.organizer_set.all()
    }, context_instance=RequestContext(request))


def add_organizer(request, bbl=None, ajax=False):
    lots = Lot.objects.filter(bbl=bbl)
    if request.method == 'POST':    
        form = OrganizerForm(request.POST)
        if form.is_valid():
            organizer = form.save()
            if ajax:
                return details_tab(request, bbl=bbl)
            else:
                return redirect('lots.views.details', bbl=bbl)
    else:
        form = OrganizerForm(initial={
            'lots': lots,
        })

    template = 'organize/add_organizer.html'
    if ajax:
        template = 'organize/add_organizer_ajax.html'

    return render_to_response(template, {
        'form': form,
        'lot': lots[0],
    }, context_instance=RequestContext(request))
