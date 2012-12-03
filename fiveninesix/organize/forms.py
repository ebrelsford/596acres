from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput, ModelChoiceField

from recaptcha_works.fields import RecaptchaField

from lots.models import Lot
from notify import notify_managers, notify_organizers_and_watchers
from models import Organizer, Watcher, Note, Picture
from widgets import PrefixLabelTextInput

class CaptchaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
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

    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        required=False,
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        # add initial value for added_by based on the user kwarg
        kwargs['initial'] = kwargs.get('initial', {})
        user = kwargs.get('user', None)
        if not user or user.is_anonymous(): user = None
        kwargs['initial']['added_by'] = user

        super(OrganizeForm, self).__init__(*args, **kwargs)

class OrganizerForm(OrganizeForm):
    class Meta:
        exclude = ('added', 'email_hash')
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
            notify_managers(organizer)
            notify_organizers_and_watchers(organizer)
        return organizer

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
