from django import template
import datetime

register = template.Library()

def ago(value):
    now = datetime.datetime.now()
    delta = now-value
    if delta.days:
        return "%s days ago" % delta.days
    elif delta.seconds>60*60:
        return "%s hours ago" % (delta.seconds/60/60)
    elif delta.seconds>60:
        return "%s minutes ago" % (delta.seconds/60)
    else:
        return "%s seconds ago" % (delta.seconds)

register.filter('ago',ago)
