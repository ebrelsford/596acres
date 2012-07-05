from django.forms import ModelForm, HiddenInput, ModelChoiceField

from recaptcha_works.fields import RecaptchaField

from lots.models import Lot
from notify import new_organizer_notify_managers, notify_organizers, notify_watchers
from models import Organizer, Watcher, Note, Picture
from widgets import PrefixLabelTextInput

class OrganizerForm(ModelForm):
    lot = ModelChoiceField(label='lot', queryset=Lot.objects.all(), widget=HiddenInput())

    recaptcha = RecaptchaField(label="Prove you're human")

    class Meta:
        model = Organizer
        widgets = {
            'facebook_page': PrefixLabelTextInput('facebook.com/'),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        is_creating = False
        if not self.instance.id:
            is_creating = True

        organizer = super(self.__class__, self).save()
        if is_creating:
            new_organizer_notify_managers(organizer)
            notify_organizers(organizer)
            notify_watchers(organizer)
        
class WatcherForm(ModelForm):
    lot = ModelChoiceField(label='lot', queryset=Lot.objects.all(), widget=HiddenInput())

    recaptcha = RecaptchaField(label="Prove you're human")

    class Meta:
        model = Watcher
        exclude = ('added', 'email_hash')
        
class NoteForm(ModelForm):
    lot = ModelChoiceField(label='lot', queryset=Lot.objects.all(), widget=HiddenInput())

    recaptcha = RecaptchaField(label="Prove you're human")

    class Meta:
        model = Note
        exclude = ('added',)
        
class PictureForm(ModelForm):
    lot = ModelChoiceField(label='lot', queryset=Lot.objects.all(), widget=HiddenInput())

    recaptcha = RecaptchaField(label="Prove you're human")

    class Meta:
        model = Picture
        exclude = ('added',)
