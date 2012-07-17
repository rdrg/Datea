from datea.datea_vote.models import DateaVote
from datea.datea_api.vote import VoteResource
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_user_votes(context):
    request = context['request']
    
    # follow keys
    votes = []
    vote_rsc = VoteResource()
    for inst in DateaVote.objects.filter(user=request.user):
        v_bundle = vote_rsc.build_bundle(obj=inst)
        v_bundle = vote_rsc.full_dehydrate(v_bundle)
        votes.append(vote_rsc.serialize(None, v_bundle, 'application/json'))
        
    return '['+",".join(votes)+']'