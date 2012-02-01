from django import template

register = template.Library()

def format_record(value):
    return "%s - %s" % (value[0],value[1])

register.filter('format_record',format_record)
