from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from forms import MailOrganizersForm
from organize import mail
from lots.models import Lot

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
    return render_to_response('fns_admin/mail_organizers_done.html', {}, context_instance=RequestContext(request))

@permission_required('lots.add_review')
def review_lots(request):
    reviewable_lots = Lot.objects.filter(is_vacant=True, owner__type__name__iexact='city', review=None)
    return render_to_response('fns_admin/review_lots.html', {
        'lots': reviewable_lots[:20],
        'count': reviewable_lots.count(),
    }, context_instance=RequestContext(request))
