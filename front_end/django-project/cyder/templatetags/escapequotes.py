from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def escapequotes(value):
    return value.replace('"', '\\"').replace("'", "\\'")
