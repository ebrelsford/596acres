from django.forms import ModelForm

from recaptcha_works.fields import RecaptchaField

from models import ContactRequest, LotInformationRequest

class RecaptchaForm(ModelForm):
    recaptcha = RecaptchaField(label="Prove you're human")

class LotInformationRequestForm(RecaptchaForm):
    class Meta:
        model = LotInformationRequest
        exclude = ('handled',)

class ContactRequestForm(RecaptchaForm):
    class Meta:
        model = ContactRequest
        exclude = ('handled',)
