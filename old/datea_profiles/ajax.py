from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string

from forms import AccountForm, ProfileForm
from views import get_edit_account_form, get_profile_detail

from django.contrib.sites.models import Site

from datea_report.models import ReportEnvironment, Category
from utils import get_object_page
from models import Profile
from django.db.models import Sum

@login_required
@dajaxice_register
def edit_account(request, env_slug, subtab):

    html = get_edit_account_form(request, env_slug, subtab, ajax=True)
    dajax = Dajax()
    dajax.assign('#my-profile-tab-content', 'innerHTML', html)
    dajax.script('Datea.hide_body_loading();')
    return dajax.json()



@login_required
@dajaxice_register
def load_my_profile(request, env_slug, subtab):
    
    environment = ReportEnvironment.objects.get(slug=env_slug)
    html = get_profile_detail(request, environment=environment, subtab=subtab, ajax=True)
    
    dajax = Dajax()
    dajax.assign('#my-profile-tab-content', 'innerHTML', html)
    dajax.script('Datea.hide_body_loading();')
    return dajax.json()


@login_required
@dajaxice_register
def load_profile(request, username=None, env_slug=None, subtab='stream'):
    
    environment = ReportEnvironment.objects.get(slug=env_slug)
    html = get_profile_detail(request, ajax=True, username=username, environment=environment, subtab=subtab)
    
    dajax = Dajax()
    dajax.assign('#profiles-detail-content', 'innerHTML', html)
    dajax.script('Datea.hide_body_loading();')
    return dajax.json()
    


@login_required
@dajaxice_register
def save_account_form(request, form):
    
    form_id = '#edit-account-form'
    
    dajax = Dajax()
    form = AccountForm(request.user, form)

    if form.is_valid():
        dajax.remove_css_class(form_id+' .clearfix','error')
        dajax.remove(form_id+' .error-msg')
        form.save()
    else:
        dajax.remove_css_class(form_id+' .clearfix','error')
        dajax.remove(form_id+' .error-msg')
        for error, message in form.errors.items():
            dajax.add_data({'selector': form_id+' #id_'+error, 'message': message.as_text()},'Datea.profiles.form_error')
    
    #dajax.add_data(form_id, 'Datea.dajax.form_process_end') 
    dajax.script('Datea.hide_body_loading();')       
    return dajax.json()



@login_required
@dajaxice_register
def save_profile_form(request, form):
    
    form_id = '#edit-profile-form'
    
    dajax = Dajax()
    
    profile = request.user.get_profile()
    form = ProfileForm(form, instance=profile)

    if form.is_valid():
        dajax.remove_css_class(form_id+' .clearfix','error')
        form.save()
    else:
        dajax.remove_css_class(form_id+' .clearfix','error')
        for error, message in form.errors.items():
            dajax.add_data({'selector': form_id+' #id_'+error, 'message': message.as_text()},'Datea.profiles.form_error')
    
    dajax.script('Datea.hide_body_loading();')  
    #dajax.add_data(form_id, 'Datea.dajax.form_process_end')          
    return dajax.json()



@dajaxice_register
def get_profile_teaser_page(request, tab_id, page_num, env_slug):
    
    dajax = Dajax()
    current_site = Site.objects.get_current()
    current_user = request.user
    current_environment = ReportEnvironment.objects.get(slug=env_slug, sites=current_site)
    
    profiles = Profile.on_site.filter(user__is_active=True) # user__is_staff = False
    if current_user.is_authenticated():
        profiles = profiles.exclude(user=current_user)
    
    if tab_id == 'tab-voted-profiles':
        sorted_profiles = profiles.annotate(vote_count=Sum('user__reports__vote_count')).filter(vote_count__gt=0).order_by('-vote_count', 'user__username')
        object_page = get_object_page(sorted_profiles, page_num)
        tab_prefix = 'voted/page/'
    elif tab_id == 'tab-commented-profiles':
        sorted_profiles = profiles.annotate(comment_count=Sum('user__reports__comment_count')).filter(comment_count__gt=0).order_by('-comment_count', 'user__username')
        object_page = get_object_page(sorted_profiles, page_num)
        tab_prefix = 'commented/page/'
    else:
        object_page = get_object_page(profiles.order_by('-user__date_joined'), page_num)
        tab_prefix = 'page/'
    
    tpl_vars = {
            'profile_list_page': object_page,
            'tab_prefix': tab_prefix,
            'environment': current_environment,
            'request': request
            }
    
    object_page_html = render_to_string("datea_profiles/_profile_list_page.html", tpl_vars, context_instance= RequestContext(request))
    
    dajax.assign('#'+tab_id+'-content', 'innerHTML', object_page_html)
    dajax.script('Datea.hide_body_loading();')
    return dajax.json()

