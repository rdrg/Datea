
from django import forms
from pinax.apps.account.utils import change_password
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from models import Profile
from emailconfirmation.models import EmailAddress

import logging
    
class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')
        
        
class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)



class UserForm(forms.Form):
    
    username = forms.CharField(required=True, label=_('Username'))
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)
        
    def clean_username(self):
        
        if self.cleaned_data['username'] != self.user.username:
            try:
                User.objects.get(username=self.cleaned_data['username'])
                raise forms.ValidationError(_("Username already taken."))
            except:
                pass
            
        return self.cleaned_data['username']
            
    def save(self):
        if self.cleaned_data['username'] != self.user.username:
            logging.info(self.cleaned_data)
            self.user.username = self.cleaned_data['username']
            self.user.save()
            
        
class AccountForm(UserForm):
    
    email = forms.EmailField(
        label = _("Email"),
        required = True,
    )
    
    password1 = forms.CharField(
        label = _("New Password"),
        widget = forms.PasswordInput(render_value=False),
        required=False
    )
    password2 = forms.CharField(
        label = _("New Password (again)"),
        widget = forms.PasswordInput(render_value=False),
        required=False
    )
    
    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password2"]
    
    def clean_email(self):
        value = self.cleaned_data["email"]
        
        # check availability
        try:
            email = EmailAddress.objects.get(email__iexact=value).exclude(user=self.user)
            raise forms.ValidationError(_("Email address already taken by another user."))
        except:
            pass
        return value
            
    
    def save(self):

        super(AccountForm, self).save()
        
        if self.cleaned_data['password1'] != '':
            change_password(self.user, self.cleaned_data["password1"])
            
        try:
            email = EmailAddress.objects.get(user=self.user)
            email.email = self.cleaned_data['email']
            email.save()
            
        except:
            # if more than one email: erase all
            emails = EmailAddress.objects.filter(user=self.user)
            for e in emails:
                e.delete()
            nu_email = EmailAddress(user=self.user, email=self.cleaned_data['email'], primary=True, verified=True)
            nu_email.save()
    
        