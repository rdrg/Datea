from django.utils.translation import ugettext, ugettext_lazy
from django.utils.html import escape, conditional_escape
from django.utils.encoding import StrAndUnicode, force_unicode
from django.forms.widgets import ClearableFileInput, CheckboxInput, Textarea 
from django.utils.safestring import mark_safe

from sorl.thumbnail import get_thumbnail

# OLWIDGET WIDGET
from olwidget.widgets import *
from olwidget import utils
import django.utils.copycompat as copy
from django.template.loader import render_to_string
from django.utils import simplejson
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe

import logging


class ImageThumbInput(ClearableFileInput):

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': '',
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'<div class="imageinput-wrap"><div class="imageinput-inputfield">%(input)s</div></div>'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            
            im = get_thumbnail(value.file, '80x80', quality=90)
            template = """
                    <div class="imageinput-wrap">
                        <table>
                            <tr><td class="initial-image">
                                %(initial)s
                            </td><td> 
                            <div class="imageinput-inputfield"><div class="changeinput-label">Cambiar:</div> %(input)s</div>
                            <div>%(clear)s borrar</div>
                            </td>
                            </tr>
                        </table>
                    </div>   
                       """

            substitutions['initial'] = (u'<div class="imageinput-thumb"><img src="%s" width="%s" height="%s" alt="" /></div>'
                                        % (escape(im.url),
                                           escape(im.width),
                                           escape(im.height)
                                           ))
            
            
            #if not self.is_required:
            checkbox_name = self.clear_checkbox_name(name)
            checkbox_id = self.clear_checkbox_id(checkbox_name)
            substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
            substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
            substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
            substitutions['clear_template'] = self.template_with_clear % substitutions

        #logging.info(template)
        #logging.info(substitutions)
        return mark_safe(template % substitutions)
        
        
        
class DateaPointLayer(BaseVectorLayer):
    """
    A wrapper for the javascript olwidget.EditableLayer() type.  Intended for
    use as a sub-widget for the Map widget.
    """
    default_template = "datea_report/olwidget/dateapoint_layer.html"
    editable = True

    def __init__(self, options=None, template=None):
        self.options = options or {}
        self.template = template or self.default_template
        super(DateaPointLayer, self).__init__()
        logging.info(self)

    def prepare(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if name and not self.options.has_key('name'):
            self.options['name'] = forms.forms.pretty_name(name)
        attrs['id'] = attrs.get('id', "id_%s" % id(self))

        wkt = utils.get_ewkt(value)
        context = {
            'id': attrs['id'],
            'options': simplejson.dumps(utils.translate_options(self.options)),
            'STATIC_URL': settings.STATIC_URL,
        }
        js = mark_safe(render_to_string(self.template, context))
        html = mark_safe(forms.Textarea().render(name, wkt, attrs))
        return (js, html)
  
  
    

        
    