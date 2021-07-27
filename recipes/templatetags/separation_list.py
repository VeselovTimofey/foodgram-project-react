from django import template

register = template.Library()


@register.filter()
def get_element(value, index):
    return value[int(index)]
