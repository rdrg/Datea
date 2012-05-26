from django import template

register = template.Library()

@register.inclusion_tag('datea_vote/_vote_widget.html', takes_context = True)
def vote_widget(context, report_object):
    
    if report_object.vote_count != None:
        vote_count = report_object.vote_count
    else:
        vote_count = 0
     
    has_voted = False
    request = context['request']
    if request.user.is_authenticated():
        try:
            my_vote = report_object.votes.get(author=request.user)
            has_voted = True
        except:
            pass
        
    return {'vote_count': vote_count, 'has_voted': has_voted, 'report': report_object}