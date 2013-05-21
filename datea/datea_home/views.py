from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _


def home(request):
    
    site = Site.objects.get_current()
    return render_to_response("datea_home/home.html", 
                {
                 'title': site.name,
                 'og_title': site.name,
                 'site': site,
                 'url': '',
                 'image': settings.OPENGRAPH_DEFAULT_IMAGE,
                 'description': _("A plattform to activate and channel community engagement. Keywords: civic engagement, social mapping, open source..."),
                 'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
                }, context_instance=RequestContext(request))





def redirect_to_hash(request, path):
    
    return HttpResponseRedirect('/#/'+path)