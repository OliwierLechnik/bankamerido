from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def remove_newlines(value):
    value = str(value)
    value = value.replace('\n', '')
    return mark_safe(value)