from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def wishlist_count(context):
    request = context['request']
    if request.user.is_authenticated:
        count = request.user.products_wishlist.count()
    else:
        count = 0
    return count
