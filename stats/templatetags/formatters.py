from django import template

register = template.Library()

def format_record(value):
    return "%s - %s" % (value[0],value[1])

def format_time(value):
    if not value:
        return None
    value = int(value)
    if value/60/60/24/7:
        return "%s weeks" % (value/60/60/24/7)
    if value/60/60/24:
        return "%s days" % (value/60/60/24)
    elif value/60/60:
        return "%s hours" % (value/60/60)
    elif value/60:
        return "%s hours" % (value/60)
    else:
        return "%s seconds" % (value)

register.filter('format_time',format_time)
register.filter('format_record',format_record)
