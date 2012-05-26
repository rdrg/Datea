from django.db import models

from follow import utils as follow_utils  
from datea_report.models import Report, ReportEnvironment, Category
from django.contrib.auth.models import User
from notification import models as notification

from follow.models import Follow
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template import Context
from django.contrib.sites.models import get_current_site
from notification.models import Notice, NoticeType

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# MODEL TO TRACK FOLLOWED OBJECTS STATE
class FollowedObjectState(models.Model):
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    notice = models.OneToOneField(Notice, related_name="followed_object_state")
    is_active = models.BooleanField(blank=True,default=True)
    
    # checking only "is_active" and "published" fields -> User, Report
    def set_active_value(self):
        try:
            self.is_active = self.content_object.is_active
        except:
            try:
                self.is_active = self.content_object.published
            except:
                pass
    
    def save(self, *args, **kwargs):
        self.set_active_value()
        super(FollowedObjectState, self).save(*args, **kwargs)

#++++++++++++++++++++++++++++++++++++++++++        
# FOLLOW OBJECT STATE UPDATE ON OBJECT SAVE
from django.db.models.signals import post_save, pre_delete

# update objects
def update_followed_object_state(sender, **kwargs):
    target_object = kwargs['instance']
    ctype = ContentType.objects.get_for_model(target_object)
    state_objects = FollowedObjectState.objects.filter(content_type=ctype, object_id=target_object.id)
    for so in state_objects:
        so.save()
        
#updating Report and User for now  (also the objects we are following)      
post_save.connect(update_followed_object_state, sender=Report)
post_save.connect(update_followed_object_state, sender=User)
    
# delete objects
def delete_followed_object_state(sender, **kwargs):
    target_object = kwargs['instance']
    ctype = ContentType.objects.get_for_model(target_object)
    state_objects = FollowedObjectState.objects.filter(content_type=ctype, object_id=target_object.id)
    for so in state_objects:
        so.delete()
pre_delete.connect(delete_followed_object_state, sender=Report)
pre_delete.connect(delete_followed_object_state, sender=User)


# registar seguimiento a modelos
follow_utils.register(Report)
follow_utils.register(User)


#++++++++++++++++++++++++++
# HELPERS
def get_all_followers_except_me(target_object, acting_user):
    recipients = []
    # get followers of target_object
    follows = Follow.objects.get_follows(target_object)
    for fol in follows:
        if fol.user != acting_user:
            recipients.append(fol.user)
        
    # get follows of acting_user
    follows = Follow.objects.get_follows(acting_user)
    for fol in follows:
        if fol.user not in recipients and fol.user != acting_user:
            recipients.append(fol.user)

    # get follows of environment (administrative users)
    try:
        users = User.objects.filter(groups=target_object.environment.admin_group, is_active=True)
        for u in users:
            recipients.append(u)
    except:
        pass
    return recipients

def build_follow_settings_link(target_object):
    
    if type(target_object) == Report:
        env_slug = target_object.environment.slug
        cat_slug = target_object.root_category().slug
        follow_settings_link = reverse('edit_notification_env',args=[env_slug])
    else:
        environment = ReportEnvironment.on_site.filter(active=True)[0]
        category = ReportEnvironment.categories.filter(parent=None)[0]
        follow_settings_link = reverse('edit_notification_env',args=[environment.slug])
        
    follow_settings_link = ''.join(['http://', str(get_current_site(None)), follow_settings_link])

def get_content_author(target_object):
    if target_object.author is not None:
        return target_object.author
    elif target_object.user is not None:
        return target_object.user
    else:
        return None
    
# notify myself without sending email
def notify_myself(target_object, user, notice_label, context):
    context_obj = Context({'sender': user, 'recipient': user})
    context_obj.update(context)
    context_obj.autoescape = True
    notice_type = NoticeType.objects.get(label=notice_label)
    own_notice_html = render_to_string('notification/'+notice_label+'/notice.html', context_instance=context_obj)
    notice = Notice.objects.create(recipient=user, message=own_notice_html,
        notice_type=notice_type, on_site=True, sender=user)
    FollowedObjectState.objects.create(notice=notice, content_object=target_object)
    
    
#++++++++++++++++++++++++++++++++++++++    
# NOTIFICATION FUNCTIONS
from notification_hack import datea_follow_notification_send_now

def notify_new_comment(target_object, comment, acting_user):
    
    recipients = get_all_followers_except_me(target_object, acting_user)
    follow_settings_link = build_follow_settings_link(target_object)
    object_name = target_object._meta.verbose_name
    object_type = target_object._meta.module_name
    content_author = get_content_author(target_object)
    
    context = {
        'target_object': target_object,
        'target_object_name': object_name,
        'target_object_type': object_type,
        'content_author': content_author,
        'comment': comment,
        'follow_settings_link': follow_settings_link,
        }
    
    if len(recipients) > 0:
        datea_follow_notification_send_now(recipients, 'new_comment', context, sender=acting_user)
    notify_myself(target_object, acting_user, 'new_comment', context)
        

def notify_new_vote(target_object, acting_user):
    
    recipients = get_all_followers_except_me(target_object, acting_user)
    follow_settings_link = build_follow_settings_link(target_object)
    object_name = target_object._meta.verbose_name
    object_type = target_object._meta.module_name
    content_author = get_content_author(target_object)
    
    context = {
        'target_object': target_object,
        'target_object_name': object_name,                                
        'target_object_type': object_type,
        'content_author': content_author,
        'follow_settings_link': follow_settings_link,
        }    
    if len(recipients) > 0:
        datea_follow_notification_send_now(recipients, 'new_vote', context, sender=acting_user)
    notify_myself(target_object, acting_user, 'new_vote', context)
    
        
def notify_new_response(target_object, response_object, acting_user):
    
    recipients = get_all_followers_except_me(target_object, acting_user)
    follow_settings_link = build_follow_settings_link(target_object)
    object_name = target_object._meta.verbose_name
    object_type = target_object._meta.module_name
    content_author = get_content_author(target_object)
    
    context = {
        'target_object': target_object,
        'target_object_name': object_name,
        'target_object_type': object_type,
        'content_author': content_author,
        'response': response_object,
        'follow_settings_link': follow_settings_link,
    }
        
    if len(recipients) > 0:
        datea_follow_notification_send_now(recipients, 'new_response', context, sender=acting_user)
    notify_myself(target_object, acting_user, 'new_response', context)
  
        
def notify_new_report(target_object, acting_user):
    
    recipients = get_all_followers_except_me(target_object, acting_user)
    follow_settings_link = build_follow_settings_link(target_object)
    object_name = target_object._meta.verbose_name
    object_type = target_object._meta.module_name
    content_author = get_content_author(target_object)
    
    context = {
        'target_object': target_object,
        'target_object_name': object_name,
        'target_object_type': object_type,
        'content_author': content_author,
        'follow_settings_link': follow_settings_link,
    }
       
    if len(recipients) > 0:
        datea_follow_notification_send_now(recipients, 'new_report', context, sender=acting_user)
    notify_myself(target_object, acting_user, 'new_report', context)
       
        
def notify_site_messages(message, acting_user):
    
    recipients = get_all_followers_except_me(message, acting_user)
    follow_settings_link = build_follow_settings_link(message)
        
    if len(recipients) > 0:
        datea_follow_notification_send_now(recipients, 'site_message', {
                                'message': message, 
                                'follow_settings_link': follow_settings_link,
                                }, sender=acting_user)
