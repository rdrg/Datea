from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

from django.contrib.sites.models import Site
from django.conf import settings
from django.forms.models import inlineformset_factory

from models import Report, Category, ReportEnvironment
from forms import ReportFormStandalone, ReportFormInsideEnv, ReportVideoFormSet
from widgets import *

import pprint
from urllib import urlencode

from django.utils import simplejson

import logging

def get_environment(env_slug, current_site):
    if env_slug == '__default__':
        try: 
            environment = ReportEnvironment.objects.filter(active=True, sites__in=[current_site])[0]
        except:
            raise Http404
    else:
        try: 
            environment = ReportEnvironment.objects.get(slug=env_slug, active=True, sites__in=[current_site])
        except:
            raise Http404
    return environment


#######################
# SHOW REPORT DETAIL
def report_detail(request, env_slug, cat_slug, report_id):
    
    current_site = Site.objects.get_current()
    current_environment = get_environment(env_slug, current_site)
    
    try:
        report = Report.objects.get(pk=report_id, published=True)
    except:
        raise Http404
    
    return render_to_response('datea_report/report_detail.html', {'report': report, 'environment': current_environment}, context_instance=RequestContext(request))
    


############################
# CREATE REPORT VIEW
def report_create(request, env_slug='__default__'):
    
    # check if user authenticated
    if not request.user.is_authenticated():
        dest = reverse('acct_login')
        return HttpResponseRedirect(dest)
    
    current_site = Site.objects.get_current()
    current_environment = get_environment(env_slug, current_site)
    
    environment_data = current_environment.get_json_environment()
    logging.info(environment_data)

    # check if data to be saved
    if request.POST:

        form = ReportFormStandalone(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            video_formset = ReportVideoFormSet(request.POST, request.FILES, instance=report)
            
            if video_formset.is_valid():
                report.author = request.user
                report.site = current_site
                report.environment = current_environment
                report.save()
                form.save_m2m()
                video_formset.save()                
                return HttpResponseRedirect(reverse('datea_report.views.report_detail', args=(report.pk,)))
        
        # SHOW VALIDATION ERRORS ON FORM
        video_formset = ReportVideoFormSet(request.POST, request.FILES)
            
        return render_to_response("datea_report/report_create.html",{
                    'form': form,
                    'video_formset': video_formset,
                    'environment_data': environment_data,
                    }, context_instance=RequestContext(request))
            
    else:
        report = Report()
        report.author = request.user
        report.site = current_site
        report.environment = current_environment
        form = ReportFormStandalone(instance=report)
        video_formset = ReportVideoFormSet(instance=report)
    
        return render_to_response("datea_report/report_create.html",{
                     "form": form, 
                     'video_formset': video_formset,
                     'environment_data': environment_data,
                     }, context_instance=RequestContext(request))


#####################
# UPDATE REPORT VIEW    
def report_update(request, report_id, env_slug='__default__'):
    
    current_site = Site.objects.get_current()
    current_environment = get_environment(env_slug, current_site)
    environment_data = current_environment.get_json_environment()
    
    report = get_object_or_404(Report, pk=report_id)
    # por seguridad, forzamos Envornment y Site
    report.site = current_site
    report.environment = current_environment

    if request.POST:

        form = ReportFormStandalone(request.POST, request.FILES, instance=report)
       
        if form.is_valid():
            report = form.save(commit=False)
            video_formset = ReportVideoFormSet(request.POST, request.FILES, instance=report)
            if video_formset.is_valid():
                form.save()
                form.save_m2m()
                video_formset.save()              
                #return HttpResponseRedirect(reverse('datea_report.views.report_detail', args=(report.pk,)))
        
        # SHOW VALIDATION ERRORS ON FORM    
        video_formset = ReportVideoFormSet(request.POST, request.FILES)

        return render_to_response("datea_report/report_create.html",{
                    "form": form,
                    'video_formset': video_formset,
                    'environment_data': environment_data,
                    }, context_instance=RequestContext(request))
            
        
    else:
        form = ReportFormStandalone(instance=report)
        video_formset = ReportVideoFormSet(instance=report)
    
    return render_to_response("datea_report/report_update.html",{
                     "form": form,
                     'video_formset': video_formset,
                     'environment_data': environment_data,
                     }, context_instance=RequestContext(request))



def home(request, active_category=None):
    
    current_site = Site.objects.get_current()
    environments = ReportEnvironment.objects.filter(active=True, sites=current_site)
    
    # no environments yet
    if len(environments) == 0:
        return render_to_response("datea_report/environment_none.html", context_instance=RequestContext(request))
    
    # single environment
    if len(environments) == 1:
        
        if request.user.is_authenticated():
            url = reverse('environment_home', args=(environments[0].slug,))
            return HttpResponseRedirect(url)
        
        active_env = environments[0]
        active_env_data = active_env.build_environment_data()
        latest_reports = Report.on_site.filter(environment=active_env, published=True).order_by('-created')[:2]
        
        tpl_vars = {
                'environment': active_env,
                'environment_data': active_env_data,
                'environment_is_home': active_category == None,
                'active_category': active_category,
                'latest_reports': latest_reports,
                }
        return render_to_response("datea_report/environment_home.html", tpl_vars, context_instance=RequestContext(request))
    
    # site with multiple report environments
    else:
        tpl_vars= {
                'environments': environments
                }
        return render_to_response("datea_report/environment_multiple.html", tpl_vars, context_instance=RequestContext(request))
 
 
def environment_tab(request, env_slug, hash_path=''):
    
    if hash_path != '':
        return HttpResponseRedirect(reverse('environment_home', args=(env_slug,))+'#/'+hash_path)
    
    template = "datea_report/environment.html"
    
    current_site = Site.objects.get_current()
    current_environment = ReportEnvironment.objects.get(slug=env_slug)
    active_category = current_environment.categories.filter(active=True)[0]
    current_environment_data  = current_environment.build_environment_data()
    current_environment_data_json  = current_environment.get_json_environment()
    
    # REPORT FORM
    if request.user.is_authenticated():
        report = Report(author=request.user, site=current_site, environment=current_environment)
        report_form = ReportFormInsideEnv(instance=report)
        report_video_formset = ReportVideoFormSet(instance=report)
    
    # GET REPORT OBJECTS
    report_objects = get_report_object_list(current_environment, current_site, [active_category.id])
    
    # REPORT PAGES: MOST RECENT, MOST VOTED, MOST COMMENTED
    reports_most_recent = get_report_page(report_objects.order_by('-created'))
    reports_most_voted  = get_report_page(report_objects.filter(vote_count__gt=0).order_by('-vote_count','-created'))
    reports_most_commented  = get_report_page(report_objects.filter(comment_count__gt=0).order_by('-comment_count','-created'))
    logging.info(reports_most_recent.paginator.num_pages)
    
    # REPORT DATA
    report_data = simplejson.dumps(build_report_data(report_objects))
    
    if request.user.is_authenticated():
        active_tab = 'my-profile'
    else:
        active_tab = 'reports'
    
    tpl_vars = {
        'environment': current_environment,
        'environment_data': current_environment_data,
        'environment_data_json': current_environment_data_json,
        'active_category': active_category,
        'active_tab': active_tab,
        'reports_most_recent': reports_most_recent,
        'reports_most_voted': reports_most_voted,
        'reports_most_commented': reports_most_commented,
        'report_data': report_data,
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
        'report_list_tab': 'recent'
        }
    if request.user.is_authenticated():
        tpl_vars.update({
            'report_form': report_form,
            'report_video_formset': report_video_formset
        })
    
    return render_to_response(template, tpl_vars, context_instance=RequestContext(request))
    


def get_report_object_list(environment, site, active_categories=[]):
    if active_categories:
        return Report.objects.filter(environment=environment, site=site, published=True, category__in =active_categories).distinct()
    else:
        return Report.objects.filter(environment=environment, site=site, published=True)
    
def get_report_page(report_list, page=1, items=5):
    paginator = Paginator(report_list, items)
    
    try:
        report_page = paginator.page(page)
    except PageNotAnInteger:
        report_page = paginator.page(1)
    except (EmptyPage, InvalidPage):
        report_page = paginator.page(paginator.num_pages)
    return report_page


def build_report_data(reports):
    data = {}
    for rep in reports:
        data[int(rep.id)] = rep.get_map_data()
    return data


from datea_report.utils import get_svg_pie_cluster, get_svg_circle

def get_pie_cluster(request):
    
    radius = request.GET['radius']
    values = request.GET['values'].split(',')
    colors = request.GET['colors'].split(',')
    
    img_path = get_svg_pie_cluster(radius, values, colors)
    img_data = open(img_path, "rb").read()
    return HttpResponse(img_data, mimetype="image/png")

def get_circle(request):
    radius = request.GET['radius']
    color = request.GET['color']
    img_path = get_svg_circle(radius, color)
    img_data = open(img_path, "rb").read()
    return HttpResponse(img_data, mimetype="image/png")
    
