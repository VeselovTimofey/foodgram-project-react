from django import template

register = template.Library()


@register.simple_tag
def tag_get_three_objects(value):
    return value[:3]
