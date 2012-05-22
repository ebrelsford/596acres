from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from forms import MailOrganizersForm
from organize import mail
from lots.models import Lot
from settings import OASIS_BASE_URL

@permission_required('organize.email_organizers')
def mail_organizers(request):
    if request.method == 'POST':    
        form = MailOrganizersForm(request.POST)
        if form.is_valid():
            mail.mail_organizers(form.data['subject'], form.data['message'])
            return redirect('fns_admin.views.mail_organizers_done')
    else:
        form = MailOrganizersForm()

    return render_to_response('fns_admin/mail_organizers.html', {
        'form': form,
    }, context_instance=RequestContext(request))

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
