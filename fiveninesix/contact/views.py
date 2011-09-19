from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from recaptcha_works.decorators import fix_recaptcha_remote_ip

from models import ContactRequest, JoinUsRequest, LotInformationRequest
from forms import ContactRequestForm, JoinUsRequestForm, LotInformationRequestForm

@fix_recaptcha_remote_ip
def join_us(request):
    if request.method == 'POST':    
        form = JoinUsRequestForm(request.POST)    
        if form.is_valid():
            join_request = form.save()
            return redirect(join_us_thanks)
    else:
        form = JoinUsRequestForm()

    return render_to_response('contact/join_us.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def join_us_thanks(request):
    return render_to_response('contact/join_us_thanks.html', {}, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def lot_info(request):
    if request.method == 'POST':    
        form = LotInformationRequestForm(request.POST)    
        if form.is_valid():
            request = form.save()
            return redirect(lot_info_thanks)
    else:
        form = LotInformationRequestForm()

    return render_to_response('contact/lot_in_your_life.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def lot_info_thanks(request):
    return render_to_response('contact/lot_in_your_life_thanks.html', {}, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def contact_us(request):
    if request.method == 'POST':    
        form = ContactRequestForm(request.POST)    
        if form.is_valid():
            request = form.save()
            return redirect(contact_us_thanks)
    else:
        form = ContactRequestForm()

    return render_to_response('contact/contact_us.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def contact_us_thanks(request):
    return render_to_response('contact/contact_us_thanks.html', {}, context_instance=RequestContext(request))

