from django.forms import ModelForm

from models import ContactRequest, JoinUsRequest, LotInformationRequest

class JoinUsRequestForm(ModelForm):
    class Meta:
        model = JoinUsRequest
        exclude = ('handled',)

class LotInformationRequestForm(ModelForm):
    class Meta:
        model = LotInformationRequest
        exclude = ('handled',)

class ContactRequestForm(ModelForm):
    class Meta:
        model = ContactRequest
        exclude = ('handled',)
