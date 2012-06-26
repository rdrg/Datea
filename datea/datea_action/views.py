# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

def redirect_to_hash(request, path):    
    return HttpResponseRedirect('/#/actions/'+path)