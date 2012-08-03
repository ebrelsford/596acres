from django.forms import ModelForm, HiddenInput, ModelChoiceField

from recaptcha_works.fields import RecaptchaField

from lots.models import Lot
from notify import new_organizer_notify_managers, notify_organizers, notify_watchers
from models import Organizer, Watcher, Note, Picture
from widgets import PrefixLabelTextInput

class CaptchaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            user = kwargs.pop('user')
        except Exception:
            user = None

        super(CaptchaForm, self).__init__(*args, **kwargs)

        # if not logged in, add recaptcha. else, do nothing.
        if not user or user.is_anonymous():
            self.fields['recaptcha'] = RecaptchaField(label="Prove you're human")

class OrganizeForm(CaptchaForm):
    lot = ModelChoiceField(
        label='lot',
        queryset=Lot.objects.all(),
        widget=HiddenInput()
    )

class OrganizerForm(OrganizeForm):
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
        
class WatcherForm(OrganizeForm):
    class Meta:
        model = Watcher
        exclude = ('added', 'email_hash')
        
class NoteForm(OrganizeForm):
    class Meta:
        model = Note
        exclude = ('added',)
        
class PictureForm(OrganizeForm):
    class Meta:
        model = Picture
        exclude = ('added',)
