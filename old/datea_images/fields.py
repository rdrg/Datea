from django.db import models
from django import forms
from .models import DateaImage
from .widgets import DateaImageM2MWidget
from django.forms.widgets import SelectMultiple, HiddenInput, MultipleHiddenInput
from django.utils.translation import ugettext_lazy as _

import logging

##############
# MODEL FIELDS

class DateaImageM2MField(models.ManyToManyField):
        
        description = _("DateaImage Many2Many Relationship")
        
        def __init__(self, to=DateaImage, max_images=3, thumbnail_size='80x80', crop=None, **kwargs):
            
            super(DateaImageM2MField, self).__init__(DateaImage, **kwargs)
            
            self.max_images = max_images
            self.thumbnail_size = thumbnail_size
            self.crop = crop
            
            
        def formfield(self, **kwargs):
            db = kwargs.pop('using', None)
            
            defaults = {
                'form_class': DateaImageM2MFormField,
                #'queryset': self.rel.to._default_manager.using(db).none(),
                'queryset': self.rel.to._default_manager.using(db).complex_filter(self.rel.limit_choices_to),
                'max_images': self.max_images,
                'thumbnail_size': self.thumbnail_size,
                'crop': self.crop
            }
            defaults.update(kwargs)
            # If initial is passed in, it's a list of related objects, but the
            # MultipleChoiceField takes a list of IDs.
            if defaults.get('initial') is not None:
                initial = defaults['initial']
                if callable(initial):
                    initial = initial()
                defaults['initial'] = [i._get_pk_val() for i in initial]
            return super(models.ManyToManyField, self).formfield(**defaults)
        
##############
# FORM FIELDS
class DateaImageM2MFormField(forms.ModelMultipleChoiceField):
    """An DateaImage MultipleChoiceField."""
    widget = DateaImageM2MWidget
    #widget = SelectMultiple
    #widget = MultipleHiddenInput
    hidden_widget = MultipleHiddenInput
    default_error_messages = {
        'list': _(u'Enter a list of values.'),
        'invalid_choice': _(u'Select a valid choice. %s is not one of the'
                            u' available choices.'),
        'invalid_pk_value': _(u'"%s" is not a valid value for a primary key.')
    }

    def __init__(self, queryset=DateaImage.objects.none(), cache_choices=False, required=True,
                 widget=None, label=None, initial=None,
                 max_images=3, thumbnail_size="80x80", crop=None,
                 help_text=None, *args, **kwargs):
        
        thumb_defaults = {
            'max_images': max_images,
            'thumbnail_size': thumbnail_size,
            'crop': crop
        }
        
        self.widget = DateaImageM2MWidget(**thumb_defaults)
        
        
        super(forms.ModelMultipleChoiceField, self).__init__(queryset, None,
            cache_choices, required, widget, label, initial, help_text,
            *args, **kwargs)
        
        
        
        