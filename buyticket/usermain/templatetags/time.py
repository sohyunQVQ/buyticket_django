from django import template
import time

register = template.Library()

@register.filter(name='timetostr')
def timetostr(value):
    timec =  time.mktime(time.strptime(value,"%Y-%m-%dT%H:%M:%SZ")) + 28800
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timec))