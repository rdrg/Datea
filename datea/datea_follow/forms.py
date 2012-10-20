from django import forms
from models import DateaNotifySettings


class DateaNotifySettingsForm(forms.ModelForm):
    class Meta:
        model = DateaNotifySettings