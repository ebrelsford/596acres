import json

from django.contrib.auth.decorators import permission_required
from django.contrib.gis.geos import Polygon
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from forms import MailOrganizersForm
from organize.mail import mass_mail_organizers, mass_mail_watchers
from organize.models import Organizer, Watcher
from lots.models import Lot
from settings import OASIS_BASE_URL

@permission_required('organize.email_organizers')
def mail_organizers(request):
    if request.method == 'POST':    
        form = MailOrganizersForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            boroughs = form.cleaned_data['boroughs']
            lot_types = form.cleaned_data['lot_types']
            owner_names = form.cleaned_data['owner_names']
            user_types = form.cleaned_data['user_types']
            bbox = form.cleaned_data['bbox']

            filters = Q(
                lot__borough__in=boroughs,
                lot__lotlayer__name__in=lot_types,
                lot__owner__name__in=owner_names,
            )

            if bbox:
                p = Polygon.from_bbox(bbox.split(','))
                filters = filters & Q(lot__centroid__within=p)

            if 'organizers' in user_types:
                organizers = Organizer.objects.filter(filters, email__isnull=False).exclude(email='')
                mass_mail_organizers(subject, message, organizers)
            if 'watchers' in user_types:
                watchers = Watcher.objects.filter(filters, email__isnull=False).exclude(email='')
                mass_mail_watchers(subject, message, watchers)
            return redirect('fns_admin.views.mail_organizers_done')
    else:
        form = MailOrganizersForm()

    return render_to_response('fns_admin/mail_organizers.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def mail_organizers_count(request):
    boroughs = request.GET.getlist('boroughs')
    lot_types = request.GET.getlist('lot_types')
    owner_names = request.GET.getlist('owner_names')
    user_types = request.GET.getlist('user_types')
    bbox = request.GET.get('bbox', None)

    lots = Lot.objects.filter(
        borough__in=boroughs,
        lotlayer__name__in=lot_types,
        owner__name__in=owner_names,
    )
    if bbox:
        p = Polygon.from_bbox(bbox.split(','))
        lots = lots.filter(centroid__within=p)

    organizers = 0
    if 'organizers' in user_types:
        # TODO in Django 1.4, could use distinct('organizer__email') ?
        organizers = len(set(lots.exclude(organizer=None).values_list('organizer__email', flat=True)))

    watchers = 0
    if 'watchers' in user_types:
        watchers = len(set(lots.exclude(watcher=None).values_list('watcher__email', flat=True)))

    counts = {
        'organizers': organizers,
        'watchers': watchers,
    }
    return HttpResponse(json.dumps(counts), mimetype='application/json')

@permission_required('organize.email_organizers')
def mail_organizers_done(request):
    return render_to_response('fns_admin/mail_organizers_done.html', {}, 
                              context_instance=RequestContext(request))

@permission_required('lots.add_review')
def review_lots(request, borough=None):
    reviewable_lots = _get_reviewable_lots(borough)
    return render_to_response('fns_admin/review_lots.html', {
        'borough': borough,
        'count': reviewable_lots.count(),
        'lots': reviewable_lots,
        'OASIS_BASE_URL': OASIS_BASE_URL,
    }, context_instance=RequestContext(request))

def _get_reviewable_lots(borough):
    return Lot.objects.filter(
        is_vacant=True,
        owner__type__name__iexact='city', 
        borough__iexact=borough,
        review=None
    ).order_by('bbl')
