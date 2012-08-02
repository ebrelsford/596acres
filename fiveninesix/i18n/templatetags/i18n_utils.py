from unidecode import unidecode

from django import template
from django.template import Node
from django.templatetags.i18n import do_translate

register = template.Library()

class AsciiTranslateNode(Node):
    def __init__(self, translate_node):
        self.translate_node = translate_node

    def render(self, context):
        rendered = self.translate_node.render(context)
        return unidecode(rendered)

def do_ascii_translate(parser, token):
    return AsciiTranslateNode(do_translate(parser, token))

register.tag('ascii_trans', do_ascii_translate)
