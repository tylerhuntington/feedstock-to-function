from django import template
import bleach
import json as jsonlib
from django.utils.safestring import mark_safe

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def json(value):
    """safe jsonify filter, bleaches the json string using the bleach html tag remover"""
    uncleaned = jsonlib.dumps(value)
    clean = bleach.clean(uncleaned)

    try:
        jsonlib.loads(clean)
    except:
        # should never happen, but this is a last-line-of-defense check
        # to make sure this blob wont get eval'ed by the JS engine as
        # anything other than a JSON object
        raise ValueError('JSON contains a quote or escape sequence that was unable to be stripped')

    return mark_safe(clean)

@register.filter(is_safe=True)
def is_numberic(value):
    return "{}".format(value).isdigit()
