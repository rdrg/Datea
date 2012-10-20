from django import forms
from models import DateaFreeCategory


class DateaFreeCategoryForm(forms.ModelForm):
    class Meta:
        model = DateaFreeCategory