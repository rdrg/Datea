from django.db.models.signals import post_save, pre_delete
from datea.datea_mapping.models import DateaMapping
from datea.datea_follow.models import DateaFollow

# Make user follow one's own action
def on_action_save(sender, instance, created, **kwargs):   
    # publish or unpublish all DateaFollow objects associated with this object
    follow_key = 'dateaaction.'+str(instance.pk)
    DateaFollow.objects.filter(follow_key=follow_key).update(published=instance.published)
        
def on_action_delete(sender, instance, **kwargs):
    DateaFollow.objects.filter(follow_key='dateaaction.'+str(instance.id)).delete()
 

def connect():  
    post_save.connect(on_action_save, sender=DateaMapping)
    #pre_delete.connect(on_action_delete, sender=DateaAction)
        