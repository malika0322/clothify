# home/templatetags/cart_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies value by arg (used for quantity * price)."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0  # Return 0 if there is an error
