from django import template

register = template.Library()

@register.filter
def stars(value):
    if value is None:
        return "☆☆☆☆☆"

    rounded = int(round(value))
    return "★" * rounded + "☆" * (5 - rounded)