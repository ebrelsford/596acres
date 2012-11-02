import logging

from django.conf import settings

import mailchimp
from mailchimp.chimpy.chimpy import ChimpyException

def subscribe(obj, is_participating=False):
    """
    Subscribe an object representing a person to the 596 Acres mailing list.
    Assumes there will be an 'email' field on the object.
    """
    if not obj or not obj.email:
        return

    merge_dict = {
        'EMAIL': obj.email,
    }

    if is_participating:
        merge_dict['GROUPINGS'] = [settings.MAILCHIMP_PARTCICIPATION_GROUP,]

    if obj.name:
        try:
            first, last = obj.name.split()
            merge_dict['FNAME'] = first
            merge_dict['LNAME'] = last
        except Exception:
            merge_dict['FNAME'] = obj.name

    if settings.DEBUG:
        logging.debug('Would be subscribing %s to the mailing list with merge_dict %s' % (obj.email, merge_dict,))
        return

    try:
        list = mailchimp.utils.get_connection().get_list_by_id(settings.MAILCHIMP_LIST_ID)
        list.subscribe(obj.email, merge_dict)
    except ChimpyException:
        # thrown if user already subscribed--ignore
        return
