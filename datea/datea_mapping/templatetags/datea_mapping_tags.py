from django import template
from datea.datea_mapping.models import DateaMapping
from datea.datea_mapping.forms import DateaMappingForm, DateaMapItemForm, DateaMapItemResponseForm

register = template.Library()


@register.assignment_tag
def get_mapping_form():
    return DateaMappingForm()

@register.assignment_tag
def get_map_item_form():
    return DateaMapItemForm()

@register.assignment_tag
def get_map_item_response_form():
    return DateaMapItemResponseForm()