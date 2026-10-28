from decimal import Decimal

from django import template

register = template.Library()


@register.filter
def qty(v):
    """Decimal('12.500') -> '12.5', Decimal('10.000') -> '10', None -> ''."""
    if v is None or v == "":
        return ""
    try:
        d = Decimal(str(v))
    except Exception:
        return v
    s = format(d.normalize(), "f")
    return s
