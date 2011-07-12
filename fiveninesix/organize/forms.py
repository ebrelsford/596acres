from django.forms import ModelForm, MultipleHiddenInput, ModelMultipleChoiceField

from lots.models import Lot
from models import Organizer

class OrganizerForm(ModelForm):
    lots = ModelMultipleChoiceField(label='lots', queryset=Lot.objects.all(), widget=MultipleHiddenInput())

    class Meta:
        model = Organizer
