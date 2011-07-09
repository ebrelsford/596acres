from django.forms import ModelForm

from models import JoinUsRequest, LotInformationRequest

class JoinUsRequestForm(ModelForm):
    class Meta:
        model = JoinUsRequest
        exclude = ('handled',)

class LotInformationRequestForm(ModelForm):
    class Meta:
        model = LotInformationRequest
        exclude = ('handled',)
