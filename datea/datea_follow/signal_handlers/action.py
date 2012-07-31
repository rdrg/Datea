from django.db.models.signals import post_save, pre_delete
from datea.datea_action.models import DateaAction
from datea.datea_follow.models import DateaFollow

# Make user follow one's own action
def on_action_save(sender, instance, created, **kwargs):
    
    if created:
        follow = DateaFollow(
                    user = instance.user,
                    follow_key = 'dateaaction.'+str(instance.id),
                    object_type = 'dateaaction',
                    object_id = instance.id
                )
        follow.save()
        
def on_action_delete(sender, instance, **kwargs):
    DateaFollow.objects.filter(follow_key='dateaaction.'+str(instance.id)).delete()
 
# NOT BEING USED!! -> action autofollow created per js and api   
#post_save.connect(on_action_save, sender=DateaAction)
#pre_delete.connect(on_action_delete, sender=DateaAction)
        