from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.auth.models import User

from datea.datea_image.models import DateaImage
from datea.datea_action.models import DateaAction
#from easy_thumbnails.files import get_thumbnailer
from sorl.thumbnail import get_thumbnail
from django.core.files.base import ContentFile
from django.conf import settings


class DateaProfile(models.Model):
    
    user = models.OneToOneField(User, verbose_name=_("User"), related_name="profile")
    created = models.DateTimeField( _('created'), auto_now_add=True)
    
    full_name = models.CharField(_("Full name"), max_length=50, null=True, blank=True)
    message = models.TextField(_('Personal Message'), max_length=140, null=True, blank=True)
    
    image = models.ForeignKey(DateaImage, blank=True, null=True, related_name="profile_image")
    image_social = models.ForeignKey(DateaImage, blank=True, null=True, related_name="profile_image_social")
    
    # statistics
    item_count = models.PositiveIntegerField(_("Item count"), default=0)
    comment_count = models.PositiveIntegerField(_('Comment count'), default=0)
    vote_count = models.PositiveIntegerField(_('Comment count'), default=0)
    #follower_count = models.PositiveIntegerField(_('Follower count'), default=0)
    #follow_count = models.PositiveIntegerField(_('Follow count'), default=0)
    
    def get_image_thumb(self, thumb_preset = 'profile_image'):
        if self.image:
            return self.image.get_thumb(thumb_preset)
        elif self.image_social:
            return self.image_social.get_thumb(thumb_preset)
        else:
            Preset = settings.THUMBNAIL_PRESETS[thumb_preset]
            url = settings.DEFAULT_PROFILE_IMAGE
            #preserve format
            ext = url.split('.')[-1].upper()
            if ext not in ['PNG', 'JPG'] or ext == 'JPG':
                ext = 'JPEG'
            options = {'format': ext }
            if 'options' in Preset:
                options.update(Preset['options'])
            return get_thumbnail(url, Preset['size'], **options).url
    
    def get_image(self):
        return self.get_image_thumb('profile_image')
    
    def get_large_image(self):
        return self.get_image_thumb('profile_image_large')
    
    def get_small_image(self):
        return self.get_image_thumb('profile_image_small')
    
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        
    def get_absolute_url(self):
        return ugettext('/profile/')+str(self.user.username)+'/'
        
    def __unicode__(self):
        name = ''
        if self.full_name != None:
            name = self.full_name
        return "%s (%s)" % (name, self.user.username)
    
    

from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in


#++++++++++++++++++++++++++++++++++++      
# SIGNALS
#
# CREATE PROFILE and Notify Settings AFTER SAVING NEW USER
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

#+++++++++++++++++++++    
# Update Twitter user and profile data with oauth response
def twitter_user_update(sender, user, response, details, **kwargs):
    profile_instance, created = DateaProfile.objects.get_or_create(user=user)
    
    if not profile_instance.full_name:
        if details['first_name'] != '' or details['last_name'] != '':
            profile_instance.full_name = details['first_name']+' '+details['last_name']
        elif details['username'] != '':
            profile_instance.full_name = details['username']
    
    # grabar imagen de avatar   
    try:
        img = urlopen(response['profile_image_url'])
        if profile_instance.image_social == None:
            img_obj = DateaImage(user=user)
            img_obj.image.save(slugify(user.username + "_tw") + '.jpg', ContentFile(img.read()))
            img_obj.save()
            profile_instance.image_social = img_obj
        else:    
            profile_instance.image_social.image.save(slugify(user.username + "_tw") + '.jpg', ContentFile(img.read()))
            profile_instance.image_social.save()
    
    except HTTPError:
        pass
    
    profile_instance.save()
    return True

pre_update.connect(twitter_user_update, sender=TwitterBackend)

#++++++++++++++++++++
# Update Facebook user and profile data with oauth values
def facebook_user_update(sender, user, response, details, **kwargs):
    profile_instance, created = DateaProfile.objects.get_or_create(user=user)
    
    f = open("/tmp/debug.txt", "w")
    f.write("details username: "+details['username']+"\n")
    f.write("user username: "+user.username+"\n")
    f.close()
    
    if not user.email:
        user.email =  details['email']
    
    if not profile_instance.full_name:    
        if details['first_name'] != '' or details['last_name'] != '':
            profile_instance.full_name = details['first_name']+' '+details['last_name']
        elif details['username'] != '':
            profile_instance.full_name = details['username']
        
    # grabar imagen de avatar
    try:        
        img_url = "http://graph.facebook.com/%s/picture?type=large" % response["id"]
        
        img = urlopen(img_url)
        if profile_instance.image_social == None:
            img_obj = DateaImage(user=user)
            img_obj.image.save(slugify(user.username + "_fb") + '.jpg', ContentFile(img.read()))
            img_obj.save()
            profile_instance.image_social = img_obj
        else:    
            profile_instance.image_social.image.save(slugify(user.username + "_fb") + '.jpg', ContentFile(img.read()))
            profile_instance.image_social.save()
    except HTTPError:
        pass
    
    profile_instance.save()
    return True

pre_update.connect(facebook_user_update, sender=FacebookBackend)

#+++++++++++++++++++++++++++++++
# Update google user and profile data with oath values
def google_user_update(sender, user, response, details, **kwargs):
    
    profile_instance, created = DateaProfile.objects.get_or_create(user=user)
    
    if not user.email:
        user.email = details['email']
        
    if not profile_instance.full_name:
        if details['first_name'] != '' or details['last_name'] != '':
            profile_instance.full_name = details['first_name']+' '+details['last_name']
        elif details['username'] != '':
            profile_instance.full_name = details['username']
    
    # grabar imagen de avatar
    try:        
        img = urlopen(response['picture'])
        if profile_instance.image_social == None:
            img_obj = DateaImage(user=user)
            img_obj.image.save(slugify(user.username + "_g") + '.jpg', ContentFile(img.read()))
            img_obj.save()
            profile_instance.image_social = img_obj
        else:    
            profile_instance.image_social.image.save(slugify(user.username + "_g") + '.jpg', ContentFile(img.read()))
            profile_instance.image_social.save()
    except HTTPError:
        pass
        
    profile_instance.save()
    return True

pre_update.connect(google_user_update, sender=GoogleOAuth2Backend)

    


