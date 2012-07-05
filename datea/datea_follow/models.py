from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from datea.datea_action.models import DateaAction
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.conf import settings

from django.db.models.signals import post_save, pre_delete

from datea.datea_comment.models import DateaComment
from datea.datea_vote.models import DateaVote
from datea.datea_mapping.models import DateaMapping, DateaMapItem


# Create your models here.

class DateaFollow(models.Model):
    
    user = models.ForeignKey(User, related_name="follows")
    created = models.DateTimeField(_('created'), auto_now_add=True)
    
    # generic content type relation to followed object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    followed_object = generic.GenericForeignKey()
    
    # a sort of natural key by which easily and fast 
    # identify the followed object and it's related historyNotices
    # for example: 'dateamapitem.15'
    follow_id = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        


class DateaNotifySettings(models.Model):
    
    user = models.OneToOneField(User, related_name="notify_settings")
    
    new_content = models.BooleanField(_('new content in my actions'), default=True)
    new_comment = models.BooleanField(_('new comment on my content'), default=True)
    new_vote = models.BooleanField(_('new vote on my content'), default=True)
     
    notice_from_site = models.BooleanField(_('general news by the site'), default=True)
    notice_from_action = models.BooleanField(_('news from actions I joined'), default=True)
    
    def get_absolute_url(self):
        return '/?edit_profile=notify_settings'
    
    def __unicode__(self):
        return _('notify settings for')+' '+self.user.username
    
    
    
def create_notify_settings(sender, instance=None, **kwargs):
    if instance is None: return
    notify_settings, created = DateaNotifySettings.objects.get_or_create(user=instance)

post_save.connect(create_notify_settings, sender=User)
        
     
        
class DateaHistoryNotice(models.Model):

    user = models.ForeignKey(User, related_name="sent_notices")
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    url = models.URLField(verify_exists=False)
    extract = models.TextField(_('Extract'), blank=True, null=True)
    
    #action = models.ForeignKey(DateaAction, blank=True, null=True, related_name="notices")
    
    # generic content type relation to the object which receives an action:
    # for example: the content which receives a vote
    receiver_type = models.ForeignKey(ContentType, null=True, blank=True, related_name="receiver_types")
    receiver_id = models.PositiveIntegerField(null=True, blank=True)
    receiver_obj = generic.GenericForeignKey('receiver_type', 'receiver_id')
    
    # generic content type relation to the acting object
    acting_type = models.ForeignKey(ContentType, null=True, blank=True, related_name="acting_types")
    acting_id = models.PositiveIntegerField(null=True, blank=True)
    acting_obj = generic.GenericForeignKey('acting_type', 'acting_id')
    
    # follow_id 
    follow_id = models.CharField(max_length=255) # can be an action or a content instance
    history_item_id =  models.CharField(max_length=255) # a content object
    
    def save(self, *args, **kwargs):
        
        if not self.extract:
            context = {
                'user': self.user,
                'receiver_object': self.receiver_obj,
                'acting_object':self.acting_obj,
                'site': Site.objects.get_current(),
                'url': self.url       
            }
            self.extract = render_to_string((
                'notice/%s/%s/extract.html' % (self.content_type.app_label, self.content_type.model), 
                'notice/extract.html'), context)
        
        self.check_published(save=False)
        super(DateaHistoryNotice, self).save(*args, **kwargs)
        
        
    def check_published(self, save=True):
        if self.receiver_object: 
            if hasattr(self.receiver_object, 'published') and self.receiver_object.published != self.published:
                self.published = self.receiver_object.published
                if save: 
                    self.save()
            elif hasattr(self.receiver_object, 'active') and self.receiver_object.active != self.published:
                self.published = self.receiver_object.active
                if save:
                    self.save()
        elif self.acting_object:
            if hasattr(self.acting_object, 'published') and self.acting_object.published != self.published:
                self.published = self.acting_object.published
                if save:
                    self.save()
            elif hasattr(self.acting_object, 'active') and self.acting_object.active != self.published:
                self.published = self.acting_object.active
                if save:
                    self.save()
        
        
    # action names at the moment: content, comment, vote
    def send_mail(self, action_name):
        # at the moment, only sending emails to owners of receiver objects
        # not sending when acting upon own content
        owner = self.receiver_object.user
        #notify_settings = owner.notify_settings
        notify_settings, created = DateaNotifySettings.objects.get_or_create(user=owner)
        
        if (getattr(owner.notify_settings, 'new_'+action_name)
            and owner != self.user 
            and owner.email):
            
            current_site = Site.objects.get_current()
            context = {
                    'user': self.user,
                    'receiver_object': self.receiver_obj,
                    'acting_object':self.acting_obj,
                    'site': current_site,
                    'url': self.url,
                    'settings_url': owner.notify_settings.get_absolute_url()       
                }
            
            mail_subject = render_to_string((
                    'notice/%s/%s/mail_subject.txt' % (self.receiver_type.app_label, self.receiver_type.model), 
                    'notice/mail_body.html'), context)
            
            mail_body = render_to_string((
                    'notice/%s/%s/mail_body.txt' % (self.receiver_type.app_label, self.receiver_type.model), 
                    'notice/mail_body.html'), context)
            
            email = EmailMessage(
                    mail_subject, 
                    mail_body, 
                    current_site.name+' <'+settings.DEFAULT_EMAIL_FROM+'>',
                    [owner.email]
                    )
            email.send()
   
   
   
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CREATE HISTORY NOTICES WITH SIGNALS FOR ALL DATEA APPS!         
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#################################
# DATEA COMMENT SIGNALS
def on_comment_save(sender, instance, created, **kwargs):
    if instance is None: return
    
    ctype = ContentType.objects.get(model=instance.object_type.lower())
    receiver_obj = ctype.get_object_for_this_type(pk=instance.object_id)
    follow_id = ctype.model+'.'+str(receiver_obj.pk)
    history_item_id = follow_id+'_dateacomment.'+str(instance.pk)
    
    if created:
        # create notice on commented object
        hist_notice = DateaHistoryNotice(
                        user=instance.user, 
                        receiver_obj=receiver_obj, 
                        acting_obj=instance,
                        url = receiver_obj.get_absolute_url()+'?comment='+str(instance.pk),
                        follow_id = follow_id,
                        history_item_id = history_item_id
                    )
        hist_notice.save()
        hist_notice.send_mail('comment')
        
        # create notice on the action, if relevant
        if hasattr(receiver_obj, 'action') or hasattr(receiver_obj, 'mapping'): # not clean: change in future
            if hasattr(receiver_obj, 'action'):
                action = getattr(receiver_obj, 'action')
            else:
                action = getattr(receiver_obj, 'mapping')
            
            action_follow_id = 'dateaaction.'+str(action.pk)
            # create notice on commented object's action
            action_hist_notice = DateaHistoryNotice(
                        user=instance.user, 
                        receiver_obj=receiver_obj, 
                        acting_obj=instance,
                        url = receiver_obj.get_absolute_url()+'?comment='+str(instance.pk),
                        follow_id = action_follow_id,
                        history_item_id = history_item_id
                    )
            action_hist_notice.save()
            if action.user != receiver_obj.user:
                action_hist_notice.send_mail('comment')
        
    else:
        hist_notice = DateaHistoryNotice.objects.get(history_item_id=history_item_id)
        hist_notice.check_published()
        
              
def on_comment_delete(sender, instance, **kwargs):
    hist_item_id =  instance.object_type.lower()+'.'+str(instance.object_id)+'_dateacomment.'+str(instance.pk)
    DateaHistoryNotice.objects.filter(history_item_id=hist_item_id).delete()


post_save.connect(on_comment_save, sender=DateaComment)
pre_delete.connect(on_comment_delete, sender=DateaComment)



############################################       
# DATEA MAP ITEM Signals 
def on_map_item_save(sender, instance, created, **kwargs):
    if instance is None: return
    
    receiver_obj = instance.mapping
    follow_id = 'dateaaction.'+str(instance.mapping.pk)
    history_item_id = follow_id+'_dateamapitem.'+str(instance.pk)
    
    if created:
        hist_notice = DateaHistoryNotice(
                        user=instance.user, 
                        receiver_obj=receiver_obj, 
                        acting_obj=instance,
                        url = instance.get_absolute_url(),
                        follow_id = follow_id,
                        history_item_id = history_item_id,
                    )
        hist_notice.save()
        hist_notice.send_mail('content')
    else:
        # publish or unpublish all DateaHistoryNotice objects 
        # associated with this mapitem 
        for hnotice in DateaHistoryNotice.objects.filter(follow_id=follow_id):
            hnotice.check_published()
        
def on_map_item_delete(sender, instance, **kwargs):
    # delete history items
    hist_item_id =  'dateaaction.'+str(instance.mapping.pk)+'_dateamapitem.'+str(instance.pk)
    DateaHistoryNotice.objects.filter(history_item_id=hist_item_id).delete()
    # delete follows on this map items
    DateaFollow.objects.filter(follow_id='dateamapitem.'+str(instance.pk)).delete()
    
post_save.connect(on_map_item_save, sender=DateaMapItem)
pre_delete.connect(on_map_item_delete, sender=DateaMapItem)



#########################################
# DATEA VOTE Signals
def on_vote_save(sender, instance, created, **kwargs):
    if instance is None: return
    
    ctype = ContentType.objects.get(model=instance.object_type.lower())
    receiver_obj = ctype.get_object_for_this_type(pk=instance.object_id)
    follow_id = ctype.model+'.'+str(receiver_obj.pk)
    history_item_id = follow_id+'_dateavote.'+str(instance.pk)
    
    if created:
        # create notice on commented object
        hist_notice = DateaHistoryNotice(
                        user=instance.user, 
                        receiver_obj=receiver_obj, 
                        acting_obj=instance,
                        url = receiver_obj.get_absolute_url(),
                        follow_id = follow_id,
                        history_item_id = history_item_id
                    )
        hist_notice.save()
        hist_notice.send_mail('vote')
        
        # create notice on the action, if relevant
        if hasattr(receiver_obj, 'action') or hasattr(receiver_obj, 'mapping'): # not clean: change in future
            if hasattr(receiver_obj, 'action'):
                action = getattr(receiver_obj, 'action')
            else:
                action = getattr(receiver_obj, 'mapping')
            
            action_follow_id = 'dateaaction.'+str(action.pk)
            # create notice on commented object's action
            action_hist_notice = DateaHistoryNotice(
                        user=instance.user, 
                        receiver_obj=receiver_obj, 
                        acting_obj=instance,
                        url = receiver_obj.get_absolute_url(),
                        follow_id = action_follow_id,
                        history_item_id = history_item_id
                    )
            action_hist_notice.save()
            if action.user != receiver_obj.user:
                action_hist_notice.send_mail('vote')
        
    else:
        hist_notice = DateaHistoryNotice.objects.get(history_item_id=history_item_id)
        hist_notice.check_published()
        
def on_vote_delete(sender, instance, **kwargs):
    hist_item_id =  instance.object_type.lower()+'.'+str(instance.object_id)+'_dateavote.'+str(instance.pk)
    DateaHistoryNotice.objects.filter(history_item_id=hist_item_id).delete()
        
post_save.connect(on_vote_save, sender=DateaVote)
pre_delete.connect(on_vote_save, sender=DateaVote)
    


    
        




    
    
    
         
    
    
    
    
    
    
    
    
    
    
        
