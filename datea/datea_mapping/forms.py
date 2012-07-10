from django import forms
from models import DateaMapping, DateaMapItem, DateaMapItemResponse


class DateaMappingForm(forms.ModelForm):
    class Meta:
        model = DateaMapping
        
class DateaMapItemForm(forms.ModelForm):
    class Meta:
        model = DateaMapItem
        
class DateaMapItemResponseForm(forms.ModelForm):
    class Meta:
        model = DateaMapItemResponse

