from django import template
from decimal import Decimal


register = template.Library()

@register.filter(name='get_star_range')
def range_filter(value):
    try:
        stars = float(value)
        return range(int(stars))
    except (ValueError, TypeError):
        return range(0)