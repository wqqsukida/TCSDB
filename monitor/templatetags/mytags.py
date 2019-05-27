from django import template

register = template.Library()

@register.filter
def get_int(s):
    s = s.replace(',','')
    return int(s)

@register.filter
def del_end(s):
    return s.split(' ')[0]

@register.filter
def class_name(s):
    return s.__class__.__name__