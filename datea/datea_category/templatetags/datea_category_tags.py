from django import template
from datea.datea_category.models import DateaCategory

register = template.Library()

@register.assignment_tag
def get_categories():
    return DateaCategory.tree.filter(active=True)