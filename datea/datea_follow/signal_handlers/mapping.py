from datea.datea_follow.models import DateaFollow, DateaHistory, DateaHistoryReceiver
from datea.datea_mapping.models import DateaMapItem, DateaMapItemResponse

from django.db.models.signals import post_save, pre_delete
from datea.datea_mapping.signals import map_item_response_created, map_item_response_updated


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
        for hitem in DateaHistory.objects.filter(history_key=history_key):
            hitem.generate_extract('dateamapitem', instance)
            hitem.check_published()
            hitem.save()
        
def on_map_item_delete(sender, instance, **kwargs):
    # delete history items
    key = 'dateaaction.'+str(instance.action.pk)+'_dateamapitem.'+str(instance.pk)
    DateaHistory.objects.filter(history_key=key).delete()
    # delete follows on this map item
    DateaFollow.objects.filter(follow_key='dateamapitem.'+str(instance.pk)).delete()



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


def on_map_item_response_update(sender, instance, **kwargs):
    map_items = instance.map_items.all()
    action = map_items[0].action
    history_key = 'dateaaction.'+str(action.pk)+'_dateamapitemresponse.'+str(instance.pk) 
    hist_item = DateaHistory.objects.get(history_key=history_key)
    hist_item.check_published()
    hist_item.generate_extract('dateamapitemresponse', instance)       
    hist_item.save()
              
def on_map_item_response_delete(sender, instance, **kwargs):
    map_items = instance.map_items.all()
    action = map_items[0].action
    key = 'dateaaction.'+str(action.pk)+'_dateamapitemresponse.'+str(instance.pk)
    DateaHistory.objects.filter(history_key=key).delete()

def connect():
    post_save.connect(on_map_item_save, sender=DateaMapItem)
    pre_delete.connect(on_map_item_delete, sender=DateaMapItem)
    map_item_response_created.connect(on_map_item_response_save, sender=DateaMapItemResponse)
    map_item_response_updated.connect(on_map_item_response_update, sender=DateaMapItemResponse)
    pre_delete.connect(on_map_item_response_delete, sender=DateaMapItemResponse)

