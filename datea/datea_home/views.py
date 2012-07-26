from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

def home(request):
    
    return render_to_response("datea_home/home.html", 
                {
                 'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
                }, context_instance=RequestContext(request))


def redirect_to_hash(request, path):
    
    return HttpResponseRedirect('/#/'+path)