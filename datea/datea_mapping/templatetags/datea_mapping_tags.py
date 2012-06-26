from django import template
from datea.datea_mapping.models import DateaMapping
from datea.datea_mapping.forms import DateaMappingForm, DateaMapItemForm

register = template.Library()


@register.assignment_tag
def get_mapping_form():
    return DateaMappingForm()

@register.assignment_tag
def get_map_item_form():
    return DateaMapItemForm()