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

from django.db.models.signals import post_save, pre_delete, m2m_changed

from datea.datea_comment.models import DateaComment
from datea.datea_vote.models import DateaVote
from datea.datea_mapping.models import DateaMapping, DateaMapItem, DateaMapItemResponse
from datea.datea_mapping.signals import map_item_response_created


# Create your models here.

class DateaFollow(models.Model):
    
    user = models.ForeignKey(User, related_name="follows")
    created = models.DateTimeField(_('created'), auto_now_add=True)
    
    # generic content type relation to followed object
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # followed_object = generic.GenericForeignKey()
    
    object_type = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()
    
    # a sort of natural key by which easily and fast 
    # identify the followed object and it's related historyNotices
    # for example: 'dateamapitem.15'
    follow_key = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        # update comment stats on voted object  
        if self.pk == None:
            ctype = ContentType.objects.get(model=self.object_type.lower())
            receiver_obj = ctype.get_object_for_this_type(pk=self.object_id)
            if hasattr(receiver_obj, 'follow_count'):
                receiver_obj.follow_count += 1
                receiver_obj.save()
        super(DateaFollow, self).save(*args, **kwargs)
       
        
    def delete(self, using=None):
        # update comment stats on voted object 
        ctype = ContentType.objects.get(model=self.object_type.lower())
        receiver_obj = ctype.get_object_for_this_type(pk=self.object_id)
        if hasattr(receiver_obj, 'follow_count'):
            receiver_obj.follow_count -= 1
            receiver_obj.save()
        super(DateaFollow, self).delete(using=using)
    
    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        


class DateaNotifySettings(models.Model):
    
    user = models.OneToOneField(User, related_name="notify_settings")
    
    new_content = models.BooleanField(_('new content in my actions'), default=True)
    new_comment = models.BooleanField(_('new comment on my content'), default=True)
    new_vote = models.BooleanField(_('new vote on my content'), default=True)
    new_reply = models.BooleanField(_('new reply on my content'), default=True)
    new_follow = models.BooleanField(_('new follower on my content'), default=True)
     
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
        
     
        
class DateaHistory(models.Model):

    user = models.ForeignKey(User, related_name="sent_notices")
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    title = models.TextField(_('Title'), blank=True, null=True)
    extract = models.TextField(_('Extract'), blank=True, null=True)
    
    history_type = models.CharField(max_length=50)
    
    # generic content type relation to the object which receives an action:
    # for example: the content which receives a vote
    #receiver_type = models.ForeignKey(ContentType, null=True, blank=True, related_name="receiver_types")
    #receiver_id = models.PositiveIntegerField(null=True, blank=True)
    #receiver_obj = generic.GenericForeignKey('receiver_type', 'receiver_id')
    
    # generic content type relation to the acting object, for example a "comment"
    acting_type = models.ForeignKey(ContentType, null=True, blank=True, related_name="acting_types")
    acting_id = models.PositiveIntegerField(null=True, blank=True)
    acting_obj = generic.GenericForeignKey('acting_type', 'acting_id')
    
    action = models.ForeignKey(DateaAction, blank=True, null=True, related_name="notices")
    
    # follow_key
    follow_key = models.CharField(max_length=255) # can be an action or a content instance
    history_key =  models.CharField(max_length=255) # a content object
    
    
    def save(self, *args, **kwargs):
        
        self.check_published(save=False)
        super(DateaHistory, self).save(*args, **kwargs)
        
    def delete(self, using=None):
        self.receiver_items.delete()
        super(DateaHistory, self).delete(using=using)
        
    def generate_extract(self, object_type, object_instance):
        context = {'instance': object_instance}
        self.extract = render_to_string('history/%s/extract.html' % object_type, context)
        
        
    def check_published(self, save=True):
        # TODO -> optimization!
        recv_pub = False
        for recv_item in self.receiver_items.all():
            if recv_item.published:
                recv_pub = True
                break
            
        if self.published != recv_pub:
            self.published = recv_pub
                
        elif self.acting_obj:
            if hasattr(self.acting_obj, 'published') and self.acting_obj.published != self.published:
                self.published = self.acting_obj.published
                
            elif hasattr(self.acting_obj, 'active') and self.acting_obj.active != self.published:
                self.published = self.acting_obj.active
                
        if save: 
            self.save()
        
        
    # context names at the moment: content, comment, vote
    def send_mail_to_receivers(self, context_name):
        # at the moment, only sending emails to owners of receiver objects
        # not sending when acting upon own content
        for instance in self.receiver_items.all():
            owner = instance.user
            #notify_settings = owner.notify_settings
            notify_settings, created = DateaNotifySettings.objects.get_or_create(user=owner)
        
            if (getattr(owner.notify_settings, 'new_'+context_name)
                and owner != self.user 
                and owner.email):
                
                current_site = Site.objects.get_current()
                context = {
                        'user': owner,
                        'receiver_obj': instance.content_obj,
                        'acting_obj': self.acting_obj,
                        'site': current_site,
                        'settings_url': owner.notify_settings.get_absolute_url()       
                }
                
                mail_subject = render_to_string(
                        'mail/%s/%s/mail_subject_owner.txt' % (instance.content_type.model, context_name), 
                        context).replace("\n",'')
                
                mail_body = render_to_string(
                        'mail/%s/%s/mail_body_owner.txt' % (instance.content_type.model, context_name), 
                        context)
                
                email = EmailMessage(
                        mail_subject, 
                        mail_body, 
                        current_site.name+' <'+settings.DEFAULT_FROM_EMAIL+'>',
                        [owner.email]
                        )
                email.send()
    
    
    def send_mail_to_action_owner(self, context_name):
        if self.action:
            owner = self.action.user
            instance = self.receiver_items.all()[0]
            
            #notify_settings = owner.notify_settings
            notify_settings, created = DateaNotifySettings.objects.get_or_create(user=owner)
        
            if (getattr(owner.notify_settings, 'new_'+context_name)
                and owner != self.user 
                and owner.email):
                
                current_site = Site.objects.get_current()
                context = {
                        'user': owner,
                        'receiver_obj': instance.content_obj,
                        'acting_obj': self.acting_obj,
                        'site': current_site,
                        'settings_url': owner.notify_settings.get_absolute_url()       
                }
                
                mail_subject = render_to_string(
                        'mail/%s/%s/mail_subject_generic.txt' % (instance.content_type.model, context_name), 
                        context).replace("\n",'')
                
                mail_body = render_to_string(
                        'mail/%s/%s/mail_body_generic.txt' % (instance.content_type.model, context_name), 
                        context)
                
                email = EmailMessage(
                        mail_subject, 
                        mail_body, 
                        current_site.name+' <'+settings.DEFAULT_FROM_EMAIL+'>',
                        [owner.email]
                        )
                email.send()
    
            
class DateaHistoryReceiver(models.Model):
    
    user = models.ForeignKey(User)
    
    name = models.CharField(_('name'), max_length=255)
    url = models.URLField(_('url'), verify_exists=False)
    
    content_type = models.ForeignKey(ContentType, null=True, blank=True, related_name="receiver_types")
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_obj = generic.GenericForeignKey('content_type', 'object_id')
    
    #object_type = models.CharField(max_length=255)
    #object_id = models.PositiveIntegerField()
    
    published = models.BooleanField(_('published'), default=True)
    
    history_item = models.ForeignKey('DateaHistory', verbose_name=_('history item'), related_name="receiver_items")
    
    
    def check_published(self, save=True):
        if self.published != self.content_obj.published and save:
            self.published = self.content_obj.published
            self.save()
        return self.published
    
            
    def save(self, *args, **kwargs):
        self.check_published(save=False)
        super(DateaHistoryReceiver, self).save(*args, **kwargs)
    
       
    def __unicode__(self):
        return self.name+' <'+self.url+'>'
     
   
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CREATE HISTORY NOTICES WITH SIGNALS FOR ALL DATEA APPS!         
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#################################
# DATEA COMMENT SIGNALS
def on_comment_save(sender, instance, created, **kwargs):
    if instance is None: return
    
    ctype = ContentType.objects.get(model=instance.object_type.lower())
    receiver_obj = ctype.get_object_for_this_type(pk=instance.object_id)
    
    follow_key = ctype.model+'.'+str(receiver_obj.pk)
    history_key = follow_key+'_dateacomment.'+str(instance.pk)
    
    if created:
        # create notice on commented object
        hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = follow_key,
                        history_key = history_key,
                        history_type = 'comment',
                    )
        if hasattr(receiver_obj, 'action'):
            hist_item.action = receiver_obj.action
        
        hist_item.generate_extract('dateacomment', instance)    
        hist_item.save()
        
        # create receiver item
        recv_item = DateaHistoryReceiver(
            user = receiver_obj.user,
            name = receiver_obj.user.username,
            url = receiver_obj.get_absolute_url(),
            content_obj = receiver_obj,
            history_item = hist_item,
        )
        recv_item.save()
        
        hist_item.send_mail_to_receivers('comment')
        
        # create notice on the action, if relevant
        if hasattr(receiver_obj, 'action'):
            
            action = getattr(receiver_obj, 'action')
            action_follow_key = 'dateaaction.'+str(action.pk)
            
            # create notice on commented object's action
            action_hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = action_follow_key,
                        history_key = history_key,
                        history_type = 'comment',
                        action = action
                    )
            action_hist_item.generate_extract('dateacomment', instance)
            action_hist_item.save()
            
            # generate receiver item
            action_recv_item = DateaHistoryReceiver(
                user = receiver_obj.user,
                name = receiver_obj.user.username,
                url = receiver_obj.get_absolute_url(),
                content_obj = receiver_obj,
                history_item = action_hist_item,
            )
            action_recv_item.save()
            
            if action.user != receiver_obj.user:
                action_hist_item.send_mail_to_action_owner('comment')
    else:
        hist_item = DateaHistory.objects.get(history_key=history_key)
        hist_item.check_published()
        
              
def on_comment_delete(sender, instance, **kwargs):
    key =  instance.object_type.lower()+'.'+str(instance.object_id)+'_dateacomment.'+str(instance.pk)
    DateaHistory.objects.filter(history_key=key).delete()


post_save.connect(on_comment_save, sender=DateaComment)
pre_delete.connect(on_comment_delete, sender=DateaComment)



############################################       
# DATEA MAP ITEM Signals 
def on_map_item_save(sender, instance, created, **kwargs):
    if instance is None: return

    follow_key = 'dateaaction.'+str(instance.action.pk)
    history_key = follow_key+'_dateamapitem.'+str(instance.pk)
    
    if created:
        # create notice on commented object
        hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = follow_key,
                        history_key = history_key,
                        history_type = 'map_item',
                        action = instance.action
                    )
        
        hist_item.generate_extract('dateamapitem', instance)    
        hist_item.save()
        
        # create receiver item
        recv_item = DateaHistoryReceiver(
            user = instance.action.user,
            name = instance.action.name,
            url = instance.get_absolute_url(),
            content_obj = instance.action,
            history_item = hist_item,
        )
        recv_item.save()
        
        hist_item.send_mail_to_action_owner('content')
    else:
        # publish or unpublish all DateaHistoryNotice objects 
        # associated with this mapitem 
        for hnotice in DateaHistory.objects.filter(follow_key=follow_key):
            hnotice.check_published()
        
def on_map_item_delete(sender, instance, **kwargs):
    # delete history items
    key = 'dateaaction.'+str(instance.action.pk)+'_dateamapitem.'+str(instance.pk)
    DateaHistory.objects.filter(history_key=key).delete()
    # delete follows on this map item
    DateaFollow.objects.filter(follow_key='dateamapitem.'+str(instance.pk)).delete()
    
post_save.connect(on_map_item_save, sender=DateaMapItem)
pre_delete.connect(on_map_item_delete, sender=DateaMapItem)


# MAP ITEM RESPONSE SIGNALS
def on_map_item_response_save(sender, instance, **kwargs):
    if instance is None: return
    
    map_items = instance.map_items.all()
    action = map_items[0].action
    history_key = 'dateaaction.'+str(action.pk)+'_dateamapitemresponse.'+str(instance.pk)

    # create notice on replied objects
    for item in map_items:
        
        follow_key = 'dateamapitem.'+str(item.pk)
        
        hist_item = DateaHistory(
                user=instance.user, 
                acting_obj=instance,
                url = item.get_absolute_url(),
                follow_key = follow_key,
                history_key = history_key,
                history_type = 'mapitemresponse',
                action = action
            )
        hist_item.generate_extract('dateamapitemresponse', instance)       
        hist_item.save()
        
        # create receiver item
        recv_item = DateaHistoryReceiver(
            user = item.action.user,
            name = item.user.username,
            url = item.get_absolute_url(),
            content_obj = item,
            history_item = hist_item,
        )
        recv_item.save()
        
        hist_item.send_mail_to_receivers('reply')
    
    # create notice on the action
    action_follow_key = 'dateaaction.'+str(action.pk)
    
    # create notice on commented object's action
    action_hist_item = DateaHistory(
                user=instance.user, 
                acting_obj=instance,
                follow_key = action_follow_key,
                history_key = history_key,
                history_type = 'mapitemresponse',
                action = action
            )
    action_hist_item.generate_extract('dateamapitemresponse', instance)
    action_hist_item.save()
    
    for item in map_items:
        # create receiver item
        recv_item = DateaHistoryReceiver(
            user = item.action.user,
            name = item.user.username,
            url = item.get_absolute_url(),
            content_obj = item,
            history_item = action_hist_item,
        )
        recv_item.save()


def on_map_item_response_update(sender, instance, created, **kwargs):
    if not created:
        map_items = instance.map_items.all()
        action = map_items[0].action
        history_key = 'dateaaction.'+str(action.pk)+'_dateamapitemresponse.'+str(instance.pk) 
        hist_item = DateaHistory.objects.get(history_key=history_key)
        hist_item.check_published()
              
def on_map_item_response_delete(sender, instance, **kwargs):
    map_items = instance.map_items.all()
    action = map_items[0].action
    key = 'dateaaction.'+str(action.pk)+'_dateamapitemresponse.'+str(instance.pk)
    DateaHistory.objects.filter(history_key=key).delete()

map_item_response_created.connect(on_map_item_response_save, sender=DateaMapItemResponse)
post_save.connect(on_map_item_response_update, sender=DateaMapItemResponse)
pre_delete.connect(on_map_item_response_delete, sender=DateaMapItemResponse)



#########################################
# DATEA VOTE Signals
def on_vote_save(sender, instance, created, **kwargs):
    if instance is None: return
    
    ctype = ContentType.objects.get(model=instance.object_type.lower())
    receiver_obj = ctype.get_object_for_this_type(pk=instance.object_id)
    follow_key = ctype.model+'.'+str(receiver_obj.pk)
    history_key = follow_key+'_dateavote.'+str(instance.pk)
    
    if created:
        # create notice on commented object
        hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = follow_key,
                        history_key = history_key,
                        history_type = 'vote',
                    )
        
        if hasattr(receiver_obj, 'action'): 
            hist_item.action = receiver_obj.action
        
        #hist_item.generate_extract('dateamapitem', receiver_obj)
        hist_item.save()
        
        # create receiver item
        recv_item = DateaHistoryReceiver(
            user = receiver_obj.user,
            name = receiver_obj.user.username,
            url = receiver_obj.get_absolute_url(),
            content_obj = receiver_obj,
            history_item = hist_item,
        )
        recv_item.save()
        
        hist_item.send_mail_to_receivers('vote')
        
        # create notice on the action, if relevant
        if hasattr(receiver_obj, 'action'): 

            action = getattr(receiver_obj, 'action')
            action_follow_key = 'dateaaction.'+str(action.pk)
            
            # create notice on voted object's action
            action_hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = action_follow_key,
                        history_key = history_key,
                        history_type = 'vote',
                        action = action
                    )
            #action_hist_item.generate_extract('dateamapitem', receiver_obj)
            action_hist_item.save()
            
            # create receiver item
            recv_item = DateaHistoryReceiver(
                user = receiver_obj.user,
                name = receiver_obj.user.username,
                url = receiver_obj.get_absolute_url(),
                content_obj = receiver_obj,
                history_item = action_hist_item,
            )
            recv_item.save()
            
            if action.user != receiver_obj.user:
                action_hist_item.send_mail_to_action_owner('vote')
        
    else:
        hist_item = DateaHistory.objects.get(history_key=history_key)
        hist_item.check_published()
        
def on_vote_delete(sender, instance, **kwargs):
    key =  instance.object_type.lower()+'.'+str(instance.object_id)+'_dateavote.'+str(instance.pk)
    DateaHistory.objects.filter(history_key=key).delete()
        
post_save.connect(on_vote_save, sender=DateaVote)
pre_delete.connect(on_vote_delete, sender=DateaVote)



#########################################
# DATEA FOLLOW Signals
def on_follow_save(sender, instance, created, **kwargs):
    if instance is None: return  
    
    ctype = ContentType.objects.get(model=instance.object_type.lower())
    receiver_obj = ctype.get_object_for_this_type(pk=instance.object_id)
    follow_key = ctype.model+'.'+str(receiver_obj.pk)
    history_key = follow_key+'_dateafollow.'+str(instance.pk)
    
    if created:
        # create notice on commented object
        hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = follow_key,
                        history_key = history_key,
                        history_type = 'follow',
                    )
        
        if hasattr(receiver_obj, 'action'): 
            hist_item.action = receiver_obj.action
        
        hist_item.save()
        
        # create receiver item
        recv_item = DateaHistoryReceiver(
            user = receiver_obj.user,
            name = receiver_obj.user.username,
            url = receiver_obj.get_absolute_url(),
            content_obj = receiver_obj,
            history_item = hist_item,
        )
        recv_item.save()
        
        hist_item.send_mail_to_receivers('follow')
        
        # create notice on the action, if relevant
        if hasattr(receiver_obj, 'action'): 

            action = getattr(receiver_obj, 'action')
            action_follow_key = 'dateaaction.'+str(action.pk)
            # create notice on commented object's action
            action_hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = action_follow_key,
                        history_key = history_key,
                        history_type = 'follow',
                        action = action
                    )
            action_hist_item.save()
            
            # create receiver item
            recv_item = DateaHistoryReceiver(
                user = receiver_obj.user,
                name = receiver_obj.user.username,
                url = receiver_obj.get_absolute_url(),
                content_obj = receiver_obj,
                history_item = action_hist_item,
            )
            recv_item.save()
            
            if action.user != receiver_obj.user:
                action_hist_item.send_mail_to_action_owner('follow')
        
    else:
        hist_item = DateaHistory.objects.get(history_key=history_key)
        hist_item.check_published()
        
def on_follow_delete(sender, instance, **kwargs):
    key =  instance.object_type.lower()+'.'+str(instance.object_id)+'_dateafollow.'+str(instance.pk)
    DateaHistory.objects.filter(history_key=key).delete()
    
post_save.connect(on_follow_save, sender=DateaFollow)
pre_delete.connect(on_follow_delete, sender=DateaFollow)
    
    
 
