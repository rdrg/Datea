from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from datea.datea_image.models import DateaImage 

class DateaProfile(models.Model):
    
    user = models.OneToOneField(User, verbose_name=_("User"))
    created = models.DateTimeField( _('created'), auto_now_add=True)
    
    first_name = models.CharField(_("First name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Last name"), max_length=50, null=True, blank=True)
    
    image = models.ForeignKey(DateaImage, blank=True, null=True, related_name="profile_image")
    image_social = models.ForeignKey(DateaImage, blank=True, null=True, related_name="profile_image_social")
    
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        
    def __unicode__(self):
        name = ''
        if self.fisrt_name != '' or self.last_name:
            name = self.fisrt_name + ' ' + self.last_name + ' '
        return name + ' ('+self.user.username+')'
    
'''    
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in



#++++++++++++++++++++++++++++++++++++      
# SIGNALS
#
# CREATE PROFILE AFTER SAVING NEW USER
def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = DateaProfile.objects.get_or_create(user=instance)
# connect to post save signal        
post_save.connect(create_profile, sender=User)



###############################################
# IMPORTS FOR DEALING WITH SOCIAL AUTH SIGNALS    
from social_auth.signals import pre_update
from social_auth.backends.twitter import TwitterBackend
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.google import GoogleOAuth2Backend

from urllib2 import urlopen, HTTPError
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile

from emailconfirmation.models import EmailAddress

import logging

# SAVE SOCIAL EMAIL
# deal with pinax email_confirmation and account app, which has a
# EmailAdress model to deal with confirmation etc 
def save_social_email(user_instance, social_email):
    all_emails = EmailAddress.objects.filter(user=user_instance)
    if len(all_emails) > 0:
        try:
            email = all_emails.get(email=social_email)
        except:
            email = all_emails.get(primary=True)
            email.email = social_email
            email.save()
    else:
        email = EmailAddress()
        email.email = social_email
        email.user = user_instance
        email.verified = True
        email.primary = True
        email.save()
        
    user_instance.email = email.email

#+++++++++++++++++++++    
# Update Twitter user and profile data with oauth response
def twitter_user_update(sender, user, response, details, **kwargs):
    profile_instance, created = Profile.objects.get_or_create(user=user)
    
    if details['first_name'] != '':
        profile_instance.first_name = details['first_name']
    if details['last_name'] != '':
        profile_instance.last_name = details['last_name']
    if profile_instance.social_uname == None and details['username'] != '':
        profile_instance.social_uname = slugify(details['username'])
        
    try:
        avatar_img = urlopen(response['profile_image_url'])
        if profile_instance.avatar == None:
            avatar = DateaImage(is_avatar=True, author=user)
            avatar.image.save(slugify(user.username + "_social") + '.jpg', ContentFile(avatar_img.read()))
            avatar.save()
            profile_instance.avatar = avatar
        else:    
            profile_instance.avatar.image.save(slugify(user.username + "_social") + '.jpg', ContentFile(avatar_img.read()))
            profile_instance.avatar.save()
    
    except HTTPError:
        pass
    
    profile_instance.save()
    return True

pre_update.connect(twitter_user_update, sender=TwitterBackend)

#++++++++++++++++++++
# Update Facebook user and profile data with oauth values
def facebook_user_update(sender, user, response, details, **kwargs):
    profile_instance, created = Profile.objects.get_or_create(user=user)
    
    save_social_email(user, details['email'])     
        
    if details['first_name'] != '':
        profile_instance.first_name = details['first_name']
    if details['last_name'] != '':
        profile_instance.last_name = details['last_name']
    if profile_instance.social_uname == None and details['username'] != '':
        profile_instance.social_uname = slugify(details['username'])
    
    # grabar imagen de avatar
    try:        
        img_url = "http://graph.facebook.com/%s/picture?type=large" % response["id"]
        avatar_img = urlopen(img_url)
        if profile_instance.avatar == None:
            avatar = DateaImage(is_avatar=True, author=user)
            avatar.image.save(slugify(user.username + "_social") + '.jpg', ContentFile(avatar_img.read()))
            avatar.save()
            profile_instance.avatar = avatar
        else:    
            profile_instance.avatar.image.save(slugify(user.username + "_social") + '.jpg', ContentFile(avatar_img.read()))
            profile_instance.avatar.save()
    except HTTPError:
        pass
    
    profile_instance.save()
    return True

pre_update.connect(facebook_user_update, sender=FacebookBackend)

#+++++++++++++++++++++++++++++++
# Update google user and profile data with oath values
def google_user_update(sender, user, response, details, **kwargs):
    
    debug = open("/home/participaya/public_html/datea3/site_media/media/debug.txt", "w")
    debug.write(str(response)+ "\r\n")
    debug.write(str(details) + "\r\n")
    debug.close()
    
    profile_instance, created = Profile.objects.get_or_create(user=user)
    
    if user.email != details['email']:
        user.email = details['email']
        defaults = {
            "user": user,
            "verified": True,
            "primary": True,
        }
        EmailAddress.objects.get_or_create(email=user.email, **defaults)
    if details['first_name'] != '':
        profile_instance.first_name = details['first_name']
    if details['last_name'] != '':
        profile_instance.last_name = details['last_name']
    if profile_instance.social_uname == None and details['username'] != '':
        profile_instance.social_uname = slugify(details['username'])
    
    # grabar imagen de avatar
    
    try:        
        avatar_img = urlopen(response['picture'])
        if profile_instance.avatar == None:
            avatar = DateaImage(is_avatar=True, author=user)
            avatar.image.save(slugify(user.username + "_social") + '.jpg', ContentFile(avatar_img.read()))
            avatar.save()
            profile_instance.avatar = avatar
        else:    
            profile_instance.avatar.image.save(slugify(user.username + "_social") + '.jpg', ContentFile(avatar_img.read()))
            profile_instance.avatar.save()
    except HTTPError:
        pass
        
    profile_instance.save()
    return True

pre_update.connect(facebook_user_update, sender=GoogleOAuth2Backend)
'''   
    


