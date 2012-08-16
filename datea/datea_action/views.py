# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

def redirect_to_hash_en(request, path):    
    return HttpResponseRedirect('/#/actions/'+path)

def redirect_to_hash_es(request, path):    
    return HttpResponseRedirect('/#/acciones/'+path)