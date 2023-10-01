from django import template

register = template.Library()


@register.filter(name='is_string')
def is_string_filter(value):
    return isinstance(value, str)
