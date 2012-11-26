from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.contrib.contenttypes.models import ContentType

from actstream import settings as actstream_settings
from actstream.actions import now
from actstream.exceptions import check_actionable_model
from actstream.models import Action

from activity_stream.managers import PlaceActionManager
from activity_stream.signals import action

class PlaceAction(Action):
    objects = PlaceActionManager()
    place = PointField(blank=True, null=True)

def place_action_handler(verb, **kwargs):
    """
    Handler function to create Action instance upon action signal call.
    """
    kwargs.pop('signal', None)

    actor = kwargs.pop('sender', None)
    if not actor: # TODO or actor.is_anonymous
        actor = User.objects.get(pk=settings.ACTIVITY_STREAM_DEFAULT_ACTOR_PK)
    check_actionable_model(actor)

    newaction = PlaceAction(
        actor_content_type=ContentType.objects.get_for_model(actor),
        actor_object_id=actor.pk,
        verb=unicode(verb),
        place=kwargs.pop('place', None), # TODO get automatically from target obj?
        public=bool(kwargs.pop('public', True)),
        description=kwargs.pop('description', None),
        timestamp=kwargs.pop('timestamp', now())
    )

    for opt in ('target', 'action_object'):
        obj = kwargs.pop(opt, None)
        if not obj is None:
            check_actionable_model(obj)
            setattr(newaction, '%s_object_id' % opt, obj.pk)
            setattr(newaction, '%s_content_type' % opt,
                    ContentType.objects.get_for_model(obj))
    if actstream_settings.USE_JSONFIELD and len(kwargs):
        newaction.data = kwargs
    newaction.save()

action.connect(place_action_handler, dispatch_uid='activity_stream.models')
