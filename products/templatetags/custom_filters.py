from django import template
from decimal import Decimal


register = template.Library()

@register.filter(name='get_star_range')
def get_star_range(value):
    try:
        stars = Decimal(value)
        return range(int(stars))
    except (ValueError, TypeError):
        return range(0)

@register.filter(name='get_empty_stars')
def get_empty_stars(value):
    try:
        stars = int(float(value))
        return range(5 - stars)
    except (ValueError, TypeError):
        return range(5)