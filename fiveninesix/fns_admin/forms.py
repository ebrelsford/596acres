from django.forms import Form, CharField, Textarea

class MailOrganizersForm(Form):
    subject = CharField()
    message = CharField(widget=Textarea)

