from django import forms
from models import DateaMapping, DateaMapItem


class DateaMappingForm(forms.ModelForm):
    class Meta:
        model = DateaMapping
        
class DateaMapItemForm(forms.ModelForm):
    class Meta:
        model = DateaMapItem

