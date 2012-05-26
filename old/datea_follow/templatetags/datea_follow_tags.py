from django import template
from follow.models import Follow
from follow import utils as follow_utils
from django.contrib.auth.models import User

from datea_follow.views import notification_settings
from notification.models import Notice

register = template.Library()

@register.inclusion_tag('datea_follow/_follow_widget.html', takes_context = True)
def follow_widget(context, object):
    
    follows = Follow.objects.get_follows(object)
    follow_count = follows.count()
    user = context['request'].user
    is_following = Follow.objects.is_following(user, object)
    object_type = 'report'
    if type(object) == User:
        object_type = 'user'
    
    return {'object': object,  'user': user, 'follow_count': follow_count, 'is_following': is_following, 'object_type': object_type}


@register.inclusion_tag('datea_follow/_follow_notification_settings.html', takes_context = True)
def follow_notification_settings(context):
    request = context['request']
    return notification_settings(request)


@register.inclusion_tag('datea_follow/_follow_activity_stream.html', takes_context = True)
def get_activity_stream(context, user):
    notices = Notice.objects.filter(recipient=user, followed_object_state__is_active=True).order_by('-added')
    return {'notices': notices}
    
    
    