from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from recaptcha_works.decorators import fix_recaptcha_remote_ip

from forms import ContactRequestForm, LotInformationRequestForm

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
            # XXX temporary fix, won't work when using other languages
            return redirect('en:contact.views.contact_us_thanks')
    else:
        form = ContactRequestForm()

    return render_to_response('contact/contact_us.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def contact_us_thanks(request):
    return render_to_response('contact/contact_us_thanks.html', {}, context_instance=RequestContext(request))

