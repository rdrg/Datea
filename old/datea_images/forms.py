from django.forms import ModelForm

from .models import DateaImage

class DateaImageForm(ModelForm):
    class Meta:
        model = DateaImage