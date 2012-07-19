from django.forms import Form, CharField, Textarea, MultipleChoiceField, CheckboxSelectMultiple

class MailOrganizersForm(Form):
    subject = CharField()
    message = CharField(widget=Textarea)

    send_to = MultipleChoiceField(
        choices=(
            ('public land', 'organizers without access on public land'),
            ('public with access', 'organizers with access on public land'),
            ('private with access', 'organizers with access on private land'),
        ),
        widget=CheckboxSelectMultiple(),
    )
