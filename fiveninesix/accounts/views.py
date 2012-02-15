from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from forms import PasswordResetForm

@csrf_protect
def password_reset(request, email=None, is_admin_site=False, template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.txt',
        html_email_template_name='registration/password_reset_email.html',
        password_reset_form=PasswordResetForm, token_generator=default_token_generator,
        post_reset_redirect=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            opts['email_template_name'] = email_template_name
            opts['html_email_template_name'] = html_email_template_name
            opts['request'] = request
            if is_admin_site:
                opts['domain_override'] = request.META['HTTP_HOST']
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form(initial={
            'email': email,
        })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

