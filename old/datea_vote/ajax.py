from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from django.template import RequestContext

from models import ReportVote
from datea_report.models import Report
from datea_follow.models import notify_new_vote 
from datea_follow.views import render_activity_stream_content

@dajaxice_register
def vote(request, report_id, val):
    
    dajax = Dajax()
    widget_id = '#vote-widget-'+str(report_id)
    
    if request.user.is_authenticated():
        report = Report.objects.get(pk=report_id)
        try:
            data = {'report_id': int(report.id)}
            
            vote, created = ReportVote.objects.get_or_create(report=report, author=request.user, defaults={'value': int(val)})
            vote.save()
            data['vote_count'] = report.vote_count = report.votes.count()
            report.save()
            
            tpl_vars = { 'has_voted': True, 'vote_count': report.vote_count, 'report': report }
            data['html'] = render_to_string('datea_vote/_vote_widget.html', tpl_vars)
            
            # update report popup and teaser
            report_data = {
                int(report.id): {
                    'teaser': render_to_string("datea_report/_report_teaser.html", {'report': report}, context_instance=RequestContext(request)),
                    'map_data': report.get_map_data()
                }
            }
            dajax.add_data({'reports': report_data}, 'Datea.report.update_report')
            
            dajax.add_data(data, 'Datea.vote.update_data')
            
            # notify vote
            notify_new_vote(report, request.user)
            # update profile activity stream
            dajax.assign('#my-profile-stream-content','innerHTML', render_activity_stream_content(request.user))
            
        except:
            dajax.script("alert('hubo un error.');")
    else:
        dajax.script("Datea.show_login_error();")
    
    dajax.script("$('"+widget_id+"').removeClass('loading');")
    
    return dajax.json()

@dajaxice_register
def unvote(request, report_id):
    
    dajax = Dajax()
    widget_id = '#vote-widget-'+str(report_id)
    
    if request.user.is_authenticated():
        try:
            report = Report.objects.get(pk=report_id)
            vote = ReportVote.objects.get(report=report, author=request.user)
            vote.delete()
            report.vote_count = report.votes.count()
            report.save()
            
            tpl_vars = { 'has_voted': False, 'vote_count': report.vote_count, 'report': report }
            html = render_to_string('datea_vote/_vote_widget.html', tpl_vars)
            dajax.add_data({'report_id': int(report.id), 'vote_count': report.vote_count, 'html': html}, 'Datea.vote.update_data')
        except:
            dajax.script("alert('hubo un error.');") 
    else:
        dajax.script("Datea.show_login_error();")    
    
    dajax.script("$('"+widget_id+"').removeClass('loading');")
    
    return dajax.json()      

