from django import template

register = template.Library()


@register.filter()
def get_element(value, index):
    return value[int(index)]


@register.simple_tag
def tag_get_element(value, index):
    return value[int(index)]
