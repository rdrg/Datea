from datea.datea_follow.models import DateaFollow, DateaHistory, DateaHistoryReceiver
from datea.datea_vote.models import DateaVote
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save, pre_delete



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
