from django.http import HttpResponseRedirect


def redirect_notify_settings(request):
    return HttpResponseRedirect('/#/?edit_profile=notify_settings')

def redirect_user(request, id):
    return HttpResponseRedirect('/#/user/'+str(id)+'/')

