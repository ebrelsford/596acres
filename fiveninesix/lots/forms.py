from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelForm, ModelChoiceField, CharField, Textarea

from organize.models import Note
from models import Lot, Review

class ReviewForm(ModelForm):
    lot = ModelChoiceField(label='lot', queryset=Lot.objects.all(), widget=HiddenInput())
    reviewer = ModelChoiceField(label='user', queryset=User.objects.all(), widget=HiddenInput())

    # Note fields
    note = CharField(required=False, help_text="anything else we should know about this lot? this will be a public note", widget=Textarea())

    class Meta:
        model = Review
        exclude = ('reviewed',)
        fields = ('lot', 'reviewer', 'in_use', 'actual_use', 'accessible', 'needs_further_review', 'nearby_lots', 'note', 'hpd_plans', 'hpd_plans_details')

    def save(self, commit=True):
        lot = self.cleaned_data['lot']

        note = Note(noter=self.cleaned_data['reviewer'].first_name, lot=lot, text=self.cleaned_data['note'])
        note.save()
        del self.cleaned_data['note']

        super(ReviewForm, self).save(commit=commit)
