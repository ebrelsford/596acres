from datetime import timedelta

from django import template
from django.utils.dateformat import format
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.filter
def eventdate(value, arg=None):
    """Format event date, taking all-day events into consideration"""
    start = value.start
    end = value.end
    full = (arg == 'full')

    all_day = False
    if start.hour == end.hour == 0:
        all_day = True # from <start> to <end>-1 day, if they're the same day just 'all day' <start>
        end = end - timedelta(days=1)

    # most common case
    if not all_day:
        out = '%s %s %s %s %s' % (
            _html_format_day(start, full=full),
            _('from'),
            _html_format_time(start, 'start'),
            _('to'),
            _html_format_time(end, 'end'),
        )
    else:
        out = ''
        if start == end:
            # all day this day
            out = _html_format_day(start, full=full)
        else:
            # all day for a series of days, just show endpoints
            out = '%s %s %s' % (
                _html_format_day(start, full=full),
                _('through'),
                _html_format_day(end, full=full),
            )
    return mark_safe(out)

def _html_format_time(dt, type='start'):
    return '<span class="when %s">%s</span>' % (type, format(dt, 'P'))

def _html_format_day(day, full=False):
    day_format = 'l, F j'
    if full:
        day_format += ', Y' # add year
    return '<span class="when day">%s</span>' % format(day, day_format)
