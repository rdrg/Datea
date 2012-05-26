from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from django.template import RequestContext

from django.contrib import comments
from django.db import models
from follow import utils as follow_utils
from follow.models import Follow

from datea_follow.models import notify_new_comment
from datea_follow.views import render_activity_stream_content


@dajaxice_register
def post_comment(request, form_data):
    
    dajax = Dajax()
    
    if request.user.is_authenticated():
        
        form_data["name"] = request.user.username
        form_data["email"] = 'cualquier@email.com'
        errors = []
        # Look up the object we're trying to comment about
        ctype = form_data.get("content_type")
        object_pk = form_data.get("object_pk")
        if ctype is None or object_pk is None:
            errors.append("Missing content_type or object_pk field.")
            
        try:
            model = models.get_model(*ctype.split(".", 1))
            target = model._default_manager.get(pk=object_pk)
        except:
            errors.append("object does not exist")
            
        form = comments.get_form()(target, data=form_data)
        
        if form.security_errors():
            errors.append("sorry, security error")
        
        if form.errors or len(errors) > 0:
            if form.errors:
                for e in form.errors:
                    errors.append(e)
            error_html = '<ul><li>'+"<li></li>".join(errors)+'</li><ul>'
            dajax.assign('#'+form_data['form_id']+' .errors','innerHTML', error_html)
            dajax.add_data('#'+form_data['form_id'], 'Datea.dajax.form_process_end')
            return dajax.json()
        
        comment = form.get_comment_object()
        comment.ip_address = request.META.get("REMOTE_ADDR", None)
        comment.user = request.user
        
        comment.save()
        
        # render comment
        context = RequestContext(request)
        
        data = { 'object_id': int(target.id), 'object_name': target._meta.module_name}
        data['comment_html'] = render_to_string('datea_comments/_comment.html', {'comment': comment }, context_instance=context)
        data['form_html'] = render_to_string('datea_comments/_comment_form.html', {'target_object': target}, context_instance=context)
        data['form_id'] = form_data['form_id']
        dajax.add_data(data, 'Datea.comments.success')
        
        # make user follow object
        follow_utils.follow(request.user, target)
        
        # update report data
        if target._meta.object_name == 'Report':
            # update follow count
            target.follow_count = Follow.objects.get_follows(target).count()
            # update comment_count
            if target.comment_count == None:
                target.comment_count = 1
            else:
                target.comment_count += 1
            target.save()
            
            report_data = {
                int(target.id): {
                    'teaser': render_to_string("datea_report/_report_teaser.html", {'report': target}, context_instance=RequestContext(request)),
                    'detail': render_to_string("datea_report/_report_detail.html", {'report': target}, context_instance=context),
                    'map_data': target.get_map_data()
                }
            }
            dajax.add_data({'reports': report_data}, 'Datea.report.update_report')
        
        # send notifications
        notify_new_comment(target, comment, request.user)
        # update profile activity stream
        dajax.assign('#my-profile-stream-content','innerHTML', render_activity_stream_content(request.user))
         
        dajax.add_data('#'+form_data['form_id'], 'Datea.dajax.form_process_end')
    else:
        dajax.script("Datea.show_login_error();")
    
    return dajax.json()
            
        
        
            
        
            