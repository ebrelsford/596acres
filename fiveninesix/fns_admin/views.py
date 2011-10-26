from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from forms import MailOrganizersForm
from organize import mail

@login_required
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

@login_required
def mail_organizers_done(request):
    return render_to_response('fns_admin/mail_organizers_done.html', {}, context_instance=RequestContext(request))
