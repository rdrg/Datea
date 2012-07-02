from tastypie.resources import ModelResource
from tastypie import fields

from datea.datea_vote.models import DateaVote

class VoteResource(ModelResource):
    
    
    class Meta:
        queryset = DateaVote.objects.all()
        resource_name = 'vote'
        allowed_methods = ['get','post','delete']
