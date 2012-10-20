from datea.datea_comment.models import DateaComment
from datea.datea_mapping.models import DateaMapItem

from django.db.models.signals import pre_delete

def on_map_item_delete(sender, instance, **kwargs):
    # delete comments
    DateaComment.objects.filter(object_type='dateamapitem', object_id=instance.id).delete()

def connect():
    pre_delete.connect(on_map_item_delete, sender=DateaMapItem)