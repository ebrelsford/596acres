from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

class PasswordResetForm(_PasswordResetForm):

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.txt',
             html_email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            text_template = loader.get_template(email_template_name)
            html_template = loader.get_template(html_email_template_name)
            c = Context({
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            })
            subject = _("Password reset on %s") % site_name
            text_content = text_template.render(c)
            html_content = html_template.render(c)
            msg = EmailMultiAlternatives(subject, text_content, None, [user.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

