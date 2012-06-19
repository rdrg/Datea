from django import forms
from models import DateaMapping


class DateaMappingForm(forms.ModelForm):
    class Meta:
        model = DateaMapping

