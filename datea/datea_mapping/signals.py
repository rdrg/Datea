from django.dispatch import Signal

map_item_response_created = Signal(providing_args=['instance'])
map_item_response_updated = Signal(providing_args=['instance'])