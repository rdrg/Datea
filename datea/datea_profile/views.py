from django.http import HttpResponseRedirect
from django.utils.translation import ugettext

def redirect_notify_settings(request):
    return HttpResponseRedirect('/#/?edit_profile=notify_settings')

def redirect_user(request, id):
    return HttpResponseRedirect('/#'+ugettext('/profile/')+str(id)+'/')

