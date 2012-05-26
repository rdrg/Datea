from django.template import Library, Node
from datea_profiles.models import Profile
from datea_report.models import Report, ReportEnvironment
from datea_profiles.utils import get_object_page
from django.contrib.sites.models import Site
from django.db.models import Sum
from django.core.urlresolvers import reverse
import re

register = Library()
     
class ProfileNode(Node):
    
    def render(self, context):
        user = context['user']
        if user.is_authenticated():
            context['profile'] = user.get_profile()
        else:
            context['profile'] = Profile()
            context['login_form']
    
        context['anonimous_image'] = 'datea/img/usuario_icono2.png'
        
        return ''
    
def get_profile(parser, token):
    return ProfileNode()
get_profile = register.tag(get_profile)



#+++++++++++++++++++++++++
# ENVIRONMENT PROFILES TAB
@register.inclusion_tag('datea_profiles/_profiles_view_tab.html', takes_context = True)
def render_profiles_tab(context, environment):
    current_user = context['request'].user
    
    profiles = Profile.on_site.filter(user__is_active=True) # user__is_staff = False
    if current_user.is_authenticated():
        profiles = profiles.exclude(user=current_user)
    
    # test query
    #profiles = list(Profile.objects.all()) * 3
    #profiles += profiles[:1]
    
    page_most_recent = get_object_page(profiles.order_by('-user__date_joined'))
    #page_most_recent = get_object_page(profiles)
    
    most_voted = profiles.annotate(vote_count=Sum('user__reports__vote_count')).filter(vote_count__gt=0).order_by('-vote_count', 'user__username')
    page_most_voted = get_object_page(most_voted)
    #page_most_voted = get_object_page(profiles)
    
    most_commented = profiles.annotate(comment_count=Sum('user__reports__comment_count')).filter(comment_count__gt=0).order_by('-comment_count', 'user__username')
    page_most_commented = get_object_page(most_commented)
    #page_most_commented = get_object_page(profiles)
    
    return {
            'profiles_most_recent': page_most_recent,
            'profiles_most_voted': page_most_voted,
            'profiles_most_commented': page_most_commented,
            'environment': environment,
            'request': context['request']
            }
    

@register.inclusion_tag('datea_profiles/_profile_detail.html', takes_context = True)
def render_full_profile(context, profile, environment):
    current_site  = Site.objects.get_current()    
    profile_reports = Report.objects.select_related('category').filter(author=profile.user, site=current_site, published=True).order_by('-created')
    request = context['request']
    return {
            'profile': profile,
            'active_user': context['request'].user,
            'environment': environment,
            'profile_reports': profile_reports,
            'site': current_site,
            'request': request
            }
    
    
@register.simple_tag(takes_context=True)
def get_login_target(context):
    
    target = '/'
    request = context['request']
    if 'next' in request.GET:
        target = request.GET['next']
    
    referer = request.META.get('HTTP_REFERER', None)
    if referer:
        referer = referer.split('?')[0]
        referer = re.sub('^https?:\/\/', '', referer).split('/')
        if referer[0] == request.META.get('HTTP_HOST') and len(referer) > 1:
            target = "/"+"/".join(referer[1:])
    
    if target in ['/account/login/','/account/signup/', '/account/password_reset', '/', '']:
        target = '/'
        current_site = Site.objects.get_current()
        environments = ReportEnvironment.objects.filter(active=True, sites=current_site)
        if len(environments) == 1:
            return reverse('environment_home', args=(environments[0].slug,))
        
    return target 



@register.simple_tag(takes_context=True)
def get_profile_url(context, profile, environment_slug=None):
    if 'request' in context:
        active_user = context['request'].user
    else:
        active_user = None
    return profile.get_absolute_url(env_slug=environment_slug, active_user=active_user)


@register.simple_tag(takes_context=True)
def get_profile_nav_url(context, profile, environment_slug=None, category_slug=None ):
    if 'request' in context:
        active_user = context['request'].user
    else:
        active_user = None
    if active_user == profile.user:
        return 'my-profile'
    else:
        return 'people/detail/'+profile.user.username
    