from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in

from datea_images.fields import DateaImageM2MField
from datea_images.models import DateaImage
    
#from sorl.thumbnail import ImageField

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


def get_current_site_id_list():
    site = Site.objects.get_current()
    return [site.id]


class Profile(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_("user"))
    
    first_name = models.CharField(_("first name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, null=True, blank=True)
    #about = models.TextField(_("about"), null=True, blank=True)
    #location = models.CharField(_("location"), max_length=40, null=True, blank=True)
    
    #avatar = DateaImageM2MField(null=True, blank=True, max_images=1, thumbnail_size="220x220", crop="smart")
    avatar = models.ForeignKey(DateaImage, blank=True, null=True)
    
    objects = models.Manager()
    on_site = CurrentSiteManager()
    sites = models.ManyToManyField(Site, default=get_current_site_id_list)

    social_uname = models.CharField(_("username (from social networks)"), max_length=50, null=True, blank=True)
    
    def count_reports(self):
        return self.user.reports.count()
    
    def count_comments(self):
        return  self.user.comment_comments.count()
    
    def count_votes(self):
        return self.user.votes.count()
    
    def count_following(self):
        return self.user.following.count()
    
    def count_followed(self):
        return self.user.get_follows().count()
    
    def __unicode__(self):
        return self.user.username
    
    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
    
    @models.permalink 
    def get_absolute_url(self, env_slug = None, active_user = None):
        if env_slug:
            if active_user and active_user == self.user:
                return ('view_profile_own_env', (), {'env_slug': env_slug })
            else:
                return ('view_profile_env', (), {'username': self.user.username, 'env_slug': env_slug})
        elif active_user and active_user == self.user:
            return ('view_profile_own_default',())
        else:
            return ('view_profile_default',(), {'username': self.username})
            
        
#++++++++++++++++++++++++++++++++++++      
# SIGNALS
#
# CREATE PROFILE AFTER SAVING NEW USER
def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)
    
    site = Site.objects.get_current()
    try:
        profile.sites.get(pk=site.pk)
    except:
        profile.sites.add(site)
        profile.save()
# connect to post save signal        
post_save.connect(create_profile, sender=User)


def check_user_site(sender, user, request, **kwargs):
    profile = user.get_profile()
    site = Site.objects.get_current()
    try:
        profile.sites.get(pk=site.pk)
    except:
        profile.sites.add(site)
        profile.save()
# connect to user login signal        
user_logged_in.connect(check_user_site)

   
    

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
    
