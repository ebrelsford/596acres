from django import forms
from django.utils.translation import ugettext_lazy as _

from recaptcha_works.fields import RecaptchaField

from models import ContactRequest, LotInformationRequest


class RecaptchaForm(forms.ModelForm):

    recaptcha = RecaptchaField(label=_("Prove you're human"))


class LotInformationRequestForm(RecaptchaForm):

    class Meta:
        model = LotInformationRequest
        exclude = ('handled',)


class ContactRequestForm(RecaptchaForm):

    class Meta:
        model = ContactRequest
        exclude = ('handled',)
        fields = ('name', 'email', 'phone', 'reason', 'borough', 'message',)
