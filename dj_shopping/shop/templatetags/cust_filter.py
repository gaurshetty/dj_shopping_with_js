from django import template
register = template.Library()


@register.filter
def truncate_n(value, n):
    return value[:n]


@register.filter
def get_range(value):
    return range(value)


@register.filter
def get_sub_range(value):
    result = 5 - value
    return range(result)


@register.filter
def get_orignal_price(val1, val2):
    result = val1 * float('1.'+str(val2))
    return "%.2f" % result


@register.filter
def list_filter(val):
    result = val.split(',')
    return result


@register.filter
def blank_table(val1, val2):
    result = val2 - val1
    return range(result)


