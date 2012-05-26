from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from datea_report.models import Report
from django.contrib.auth.models import User
from follow import utils as follow_utils
from follow.models import Follow
from django.template import RequestContext

from views import notification_settings


@dajaxice_register
def follow(request, object_type, object_id, action):
    
    dajax = Dajax()
    widget_id = '#follow-widget-'+str(object_type)+'-'+str(object_id)
    
    if request.user.is_authenticated():
        if object_type == 'report':
            instance = Report.objects.get(pk=int(object_id))
        else:
            instance = User.objects.get(pk=int(object_id))
        
        data = {'object_id': int(instance.id), 'object_type': object_type}
        
        if action == 'follow':    
            follow_utils.follow(request.user, instance)
            is_following = True
        else:
            follow_utils.unfollow(request.user, instance)
            is_following = False
        
        follows = Follow.objects.get_follows(instance)
        data['follow_count'] = follows.count()
        
        if object_type == 'report':
            instance.follow_count = data['follow_count']
            instance.save()   
            # update report popup and teaser
            report_data = {
                int(instance.id): {
                    'teaser': render_to_string("datea_report/_report_teaser.html", {'report': instance}, context_instance=RequestContext(request)),
                    'map_data': instance.get_map_data()
                }
            }
            dajax.add_data({'reports': report_data}, 'Datea.report.update_report')
        
        tpl_tags = {'object': instance, 'follow_count': data['follow_count'], 'is_following': is_following, 'object_type': object_type, 'user': request.user}
        data['html'] = render_to_string("datea_follow/_follow_widget.html", tpl_tags)
        dajax.add_data(data, 'Datea.follow.update_data')
    else:
        dajax.script("Datea.show_login_error();")
        
    dajax.script("$('"+widget_id+"').removeClass('loading');")
    return dajax.json()


@login_required
@dajaxice_register
def save_notification_settings(request, form_data):
    dajax = Dajax()
    
    request.POST = form_data
    settings = notification_settings(request)
    html = render_to_string('datea_follow/_follow_notification_settings.html', settings, context_instance=RequestContext(request))
    
    dajax.assign('#edit-notification-tab-content', 'innerHTML', html)
    dajax.script("Datea.hide_body_loading();")
    return dajax.json()


    
