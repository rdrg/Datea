from datea.datea_follow.models import DateaFollow, DateaHistory, DateaHistoryReceiver
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save, pre_delete


#########################################
# DATEA FOLLOW Signals
def on_follow_save(sender, instance, created, **kwargs):
    if instance is None: return  
    
    ctype = ContentType.objects.get(model=instance.object_type.lower())
    receiver_obj = ctype.get_object_for_this_type(pk=instance.object_id)
    follow_key = ctype.model+'.'+str(receiver_obj.pk)
    history_key = follow_key+'_dateafollow.'+str(instance.pk)
    
    # don't create notices on following one's own objects
    if instance.user != receiver_obj.user:
        return
    
    if created:
        # create notice on commented object
        
        recv_type = receiver_obj.get_api_name(mode='base')
        
        hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = follow_key,
                        history_key = history_key,
                        sender_type = 'follow',
                        receiver_type = recv_type,
                    )
        
        if hasattr(receiver_obj, 'action'): 
            hist_item.action = receiver_obj.action
        
        hist_item.save()
        
        # create receiver item
        if recv_type == 'action':
            recv_name = receiver_obj.name
        else:
            recv_name = receiver_obj.user.username
        
        recv_item = DateaHistoryReceiver(
            user = receiver_obj.user,
            name = recv_name,
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
                        sender_type = 'follow',
                        receiver_type = receiver_obj.get_api_name(mode='base'),
                        action = action
                    )
            action_hist_item.save()
            
            # create receiver item
            recv_item = DateaHistoryReceiver(
                user = receiver_obj.user,
                name = recv_name,
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

def connect():
    post_save.connect(on_follow_save, sender=DateaFollow)
    pre_delete.connect(on_follow_delete, sender=DateaFollow)

