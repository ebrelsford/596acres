from django import template
from django.conf import settings
from django.template.loader import render_to_string

from classytags.arguments import Argument
from classytags.core import Options, Tag

register = template.Library()

class LikeButton(Tag):
    name = 'like_button'
    options = Options(
        Argument('url'),
    )

    def render_tag(self, context, url):
        return render_to_string('facebook/like_button.html', {
            'BASE_URL': settings.BASE_URL,
            'url': url,
        })

register.tag(LikeButton)


class ShareButton(Tag):
    name = 'share_button'
    options = Options(
        Argument('url'),
    )

    def render_tag(self, context, url):
        return render_to_string('facebook/share_button.html', {
            'BASE_URL': settings.BASE_URL,
            'url': url,
        })

register.tag(ShareButton)
