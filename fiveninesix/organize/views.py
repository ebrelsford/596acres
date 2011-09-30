import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from recaptcha_works.decorators import fix_recaptcha_remote_ip

from lots.models import Lot
from forms import OrganizerForm, WatcherForm, NoteForm, PictureForm
from models import Organizer

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


@fix_recaptcha_remote_ip
def add_organizer(request, bbl=None):
    lots = Lot.objects.filter(bbl=bbl)
    if request.method == 'POST':    
        form = OrganizerForm(request.POST)
        if form.is_valid():
            organizer = form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = OrganizerForm(initial={
            'lots': lots,
        })

    template = 'organize/add_organizer.html'

    return render_to_response(template, {
        'form': form,
        'lot': lots[0],
    }, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def add_watcher(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':    
        form = WatcherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = WatcherForm(initial={
            'lot': lot,
        })

    template = 'organize/add_watcher.html'

    return render_to_response(template, {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def add_note(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':    
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = NoteForm(initial={
            'lot': lot,
        })

    template = 'organize/add_note.html'

    return render_to_response(template, {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def add_picture(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':    
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = PictureForm(initial={
            'lot': lot,
        })

    template = 'organize/add_picture.html'

    return render_to_response(template, {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def edit_organizer(request, bbl=None, id=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    organizer = get_object_or_404(Organizer, id=id)

    if request.method == 'POST':    
        form = OrganizerForm(request.POST, instance=organizer)
        if form.is_valid():
            organizer = form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = OrganizerForm(instance=organizer)

    return render_to_response('organize/edit_organizer.html', {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

def delete_organizer(request, bbl=None, id=None):
    organizer = get_object_or_404(Organizer, id=id)
    organizer.delete()

    return redirect('lots.views.details', bbl=bbl)
