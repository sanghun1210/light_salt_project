import os
import urllib.parse
from django import template


register = template.Library()

@register.filter
def getFilename(value):
    return os.path.basename(value)

@register.filter
def setQuote(value):
    return urllib.parse.quote(value)

@register.filter
def unsetQuote(value):
    return urllib.parse.unquote(value)

@register.filter
def multiply(value, arg):
    return value*arg

@register.filter
def times(value):
    return range(value)

@register.filter
def enumerates(value):
    return enumerate(value)

@register.filter
def remainder(value, divisor):
    return (value+1) % divisor
