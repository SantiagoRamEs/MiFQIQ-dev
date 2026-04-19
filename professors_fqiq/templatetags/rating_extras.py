from django import template

register = template.Library()

#RATING
@register.filter
def stars(value):
    if value is None:
        return "☆☆☆☆☆"

    rounded = int(round(value))
    return "★" * rounded + "☆" * (5 - rounded)

#NAMES-COMMENTS
@register.filter
def first_word(value):
    if value:
        return value.split()[0]
    return ''