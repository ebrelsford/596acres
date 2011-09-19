from django.core.mail import mail_managers
from django.core.urlresolvers import reverse
from django.forms import ModelForm, MultipleHiddenInput, ModelMultipleChoiceField

from recaptcha_works.fields import RecaptchaField

from lots.models import Lot
from models import Organizer
from settings import BASE_URL
from widgets import PrefixLabelTextInput

class OrganizerForm(ModelForm):
    lots = ModelMultipleChoiceField(label='lots', queryset=Lot.objects.all(), widget=MultipleHiddenInput())

    recaptcha = RecaptchaField(label="Prove you're human")

    class Meta:
        model = Organizer
        widgets = {
            'facebook_page': PrefixLabelTextInput('facebook/'),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        organizer = super(self.__class__, self).save()
        self._send_notification(organizer)

    def _send_notification(self, organizer):
        lots_urls = [BASE_URL + reverse('lots.views.details', args=(l.bbl,)) for l in organizer.lots.all()]
        message = """Neat! A new organizer was created on 596acres.org.

Details:
name: %s
type: %s
phone: %s
email: %s
url: %s
lots: %s
""" % (organizer.name, organizer.type.name, organizer.phone, organizer.email, organizer.url, ', '.join(lots_urls),)

        mail_managers('A new organizer was created on 596acres.org', message)
