from datea.datea_follow.models import DateaFollow 
from datea.datea_api.follow import NotifySettingsResource, FollowResource
from datea.datea_follow.forms import DateaNotifySettingsForm 
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_user_follows(context):
    request = context['request']
    
    # follow keys
    follows = []
    follow_rsc = FollowResource()
    for f in DateaFollow.objects.filter(user=request.user, published=True):
        f_bundle = follow_rsc.build_bundle(obj=f)
        f_bundle = follow_rsc.full_dehydrate(f_bundle)
        follows.append(follow_rsc.serialize(None, f_bundle, 'application/json'))
        
    return '['+",".join(follows)+']'


@register.simple_tag(takes_context=True)
def get_user_notify_settings(context):
    request = context['request']
    # notify_settings
    nsettings_rsc = NotifySettingsResource()
    nsettings_bundle = nsettings_rsc.build_bundle(obj=request.user.notify_settings)
    nsettings_bundle = nsettings_rsc.full_dehydrate(nsettings_bundle)
    return nsettings_rsc.serialize(None, nsettings_bundle, 'application/json')


@register.assignment_tag
def get_notify_settings_form():
    return DateaNotifySettingsForm()