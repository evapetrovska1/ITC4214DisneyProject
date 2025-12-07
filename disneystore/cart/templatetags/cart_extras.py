from django import template

register = template.Library()

# Register the multiply filter that is used in the html
@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0