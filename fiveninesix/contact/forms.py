from django.forms import ModelForm

from recaptcha_works.fields import RecaptchaField

from models import ContactRequest, JoinUsRequest, LotInformationRequest

class RecaptchaForm(ModelForm):
    recaptcha = RecaptchaField(label="Prove you're human")

class JoinUsRequestForm(RecaptchaForm):
    class Meta:
        model = JoinUsRequest
        exclude = ('handled',)

class LotInformationRequestForm(RecaptchaForm):
    class Meta:
        model = LotInformationRequest
        exclude = ('handled',)

class ContactRequestForm(RecaptchaForm):
    class Meta:
        model = ContactRequest
        exclude = ('handled',)
