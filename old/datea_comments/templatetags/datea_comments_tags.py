from django import template

register = template.Library()

@register.filter
def get_modulename(model):
    return model._meta.module_name