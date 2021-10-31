import copy
from django import template

register = template.Library()


@register.simple_tag
def get_list_of_tags(new_tag, old_tags, minus=False):
    current_tags = copy.deepcopy(old_tags)
    if minus:
        current_tags.remove(new_tag)
    else:
        current_tags.append(new_tag)
    tags = ""
    for tag in current_tags:
        tags += f"{tag} "
    if not tags:
        tags = "Нет тегов"
    return tags
