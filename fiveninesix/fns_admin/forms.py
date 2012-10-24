from django.db.models import Q
from django.forms import Form, CharField, Textarea, MultipleChoiceField,\
        HiddenInput, CheckboxSelectMultiple

from lots.models import Lot

class MailOrganizersForm(Form):
    subject = CharField()
    message = CharField(widget=Textarea)

    bbox = CharField(required=False, widget=HiddenInput)

    boroughs = MultipleChoiceField(
        choices=(), # set in __init__
        widget=CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    lot_types = MultipleChoiceField(
        choices=(
            ('vacant_sites', 'vacant public sites'),
            ('organizing_sites', 'public sites being organized around'),
            ('public_accessed_sites', 'public sites that have been accessed'),
            ('private_accessed_sites', 'private sites that have been accessed'),
            #('garden_sites', 'pre-596 community gardens'),
            ('gutterspace', 'gutterspace'),
        ),
        initial=(
            'organizing_sites',
            'private_accessed_sites',
            'public_accessed_sites',
            'vacant_sites',
        ),
        widget=CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    owner_names = MultipleChoiceField(
        choices=(), # set in __init__
        widget=CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    user_types = MultipleChoiceField(
        choices=(
            ('organizers', 'organizers'),
            ('watchers', 'watchers'),
        ),
        initial=('organizers', 'watchers'),
        widget=CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    def __init__(self, *args, **kwargs):
        super(MailOrganizersForm, self).__init__(*args, **kwargs)

        lots = Lot.objects.filter(
            ~Q(organizer=None) | ~Q(watcher=None),
        )

        owner_names = sorted(list(set(lots.values_list('owner__name', flat=True))))
        self.fields['owner_names'].choices = [(o, o) for o in owner_names]
        self.fields['owner_names'].initial = owner_names

        boroughs = sorted(list(set(lots.values_list('borough', flat=True))))
        self.fields['boroughs'].choices = [(b, b) for b in boroughs]
        self.fields['boroughs'].initial = boroughs
