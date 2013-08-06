from datetime import datetime

from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput, ModelChoiceField

from django_monitor.conf import PENDING_STATUS, APPROVED_STATUS
from django_monitor.models import MonitorEntry
from recaptcha_works.fields import RecaptchaField

from lots.models import Lot
from notify import notify_organizers_and_watchers, notify_facilitators
from mailutils import mail_facilitators
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
        organizer = super(OrganizerForm, self).save()
        status = PENDING_STATUS

        # Automoderate
        monitor_entry = MonitorEntry.objects.create(
            content_object=organizer,
            timestamp=datetime.now()
        )
        monitor_entry.moderate(status, None)

        # Notify facilitators that this organizer needs moderation
        mail_facilitators('New organizer needs moderation',
            message_template='organize/notifications/moderate_organizer.txt',
            borough=organizer.lot.borough,
            lot=organizer.lot,
            organizer=organizer,
        )
        return organizer


class WatcherForm(OrganizeForm):
    class Meta:
        model = Watcher
        exclude = ('added', 'email_hash')


class NoteForm(OrganizeForm):
    class Meta:
        model = Note
        exclude = ('added',)

    def save(self, force_insert=False, force_update=False, commit=True):
        note = super(NoteForm, self).save()
        user = note.added_by
        status = PENDING_STATUS

        if user and user.is_authenticated() and user.is_staff:
            status = APPROVED_STATUS

        # Automoderate
        monitor_entry = MonitorEntry.objects.create(
            content_object=note,
            timestamp=datetime.now()
        )
        monitor_entry.moderate(status, user)

        if status == PENDING_STATUS:
            # Notify facilitators that this note needs moderation
            mail_facilitators('New note needs moderation',
                message_template='organize/notifications/moderate_note.txt',
                borough=note.lot.borough,
                lot=note.lot,
                note=note,
            )
        return note


class PictureForm(OrganizeForm):
    class Meta:
        model = Picture
        exclude = ('added',)
