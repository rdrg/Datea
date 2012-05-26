# Create your views here.
#from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.contrib.auth.models import User
from models import Profile
from forms import AccountForm, ProfileForm, AvatarForm
from datea_images.forms import DateaImageForm
from datea_images.models import DateaImage
from datea_report.models import Report

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template import RequestContext

from django.contrib.sites.models import Site

from django.contrib import messages


'''
class datea_profile_detail(DetailView):
    template_name = 1 
'''

def get_edit_account_form(request, env_slug=None, subtab="account", ajax=False):
    # ACCOUNT FORM
    try:
        address = request.user.emailaddress_set.all()[0].email
    except:
        address = ''
        
    form_init = {
        'username': request.user.username,
        'email': address
    }
    accountform = AccountForm(request.user, initial=form_init)
    
    # PROFILE FORM
    profileform = ProfileForm(instance=request.user.get_profile())

    tpl_vars = {
                'accountform': accountform,
                'profileform': profileform,
                'env_slug': env_slug,
                'subtab': subtab
                }
    
    if ajax==False:
        template = 'datea_profiles/edit_account.html'
    else:
        template = 'datea_profiles/_edit_account.html'
    
    return render_to_string(template, tpl_vars, 
                              context_instance=RequestContext(request))
  
    
def get_profile_detail(request, username=None, environment=None, subtab="stream", ajax=False):
    
    if username != None:
        profile = Profile.objects.get(user__username=username)
    else:
        profile = request.user.get_profile()
    
    if ajax==False:
        template = 'datea_profiles/profile_detail.html'
    else:
        template = 'datea_profiles/_profile_detail.html'
    
    current_site  = Site.objects.get_current()    
    profile_reports = Report.objects.filter(author=profile.user, site=current_site, published=True).order_by('-created')
    
    tpl_vars = {
                 'profile': profile, 
                 'active_user': request.user,
                 'profile_is_active_user': request.user == profile.user,
                 'environment': environment, 
                 'profile_reports': profile_reports,
                 'subtab': subtab,
                 'request': request,
                 'site': current_site
                }
    
    return render_to_string(template, tpl_vars, 
                              context_instance=RequestContext(request))    
    
    
    
@login_required    
def edit_account(request):
    response = get_edit_account_form(request)
    return HttpResponse(response)



@login_required
def view_profile(request, username = None, env_slug=None):
    response = get_profile_detail(request)
    return HttpResponse(response)
   
    
@login_required   
def upload_avatar(request):
    
    profile = request.user.get_profile()
    if profile.avatar is not None:
        avatar = profile.avatar
    else:
        avatar = DateaImage(is_avatar=True, author=request.user)
    
    form = DateaImageForm(request.POST, request.FILES, instance=avatar)
    
    if form.is_valid():
        avatar = form.save()
        profile.avatar = avatar
        profile.save()
        return render_to_response('datea_profiles/_render_new_avatar.html', {'avatar': avatar}, 
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse("Error: Intente nuevamente.")
        
        
    
        
    
