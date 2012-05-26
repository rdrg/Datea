# -*- coding: utf-8 -*-
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string

from forms import ReportFormInsideEnv, ReportVideoFormSet, ReportEnvAdminForm
from models import ReportEnvironment, Report, Category

from django.contrib.sites.models import Site
from follow import utils as follow_utils
from datea_follow.models import notify_new_report
from datea_follow.views import render_activity_stream_content
from views import get_report_object_list, get_report_page, build_report_data


@login_required
@dajaxice_register
def save_report(request, form_data):
    
    dajax = Dajax()
    errors = {}
    
    #try:
    current_site = Site.objects.get_current()
    current_environment = ReportEnvironment.objects.get(pk=form_data['environment'], sites=current_site)
    report_form = ReportFormInsideEnv(form_data)
    
    if report_form.is_valid():
        
        report = report_form.save(commit=False)
        video_formset = ReportVideoFormSet(form_data, instance=report)
        if video_formset.is_valid():
            
            report.author = request.user # asegurarse de quien es el autor
            report.site = current_site # lo mismo para site environment
            report.environment = current_environment
            report.status = 'new'
            
            report.save()
            report_form.save_m2m()
            video_formset.save()
            
            # follow own report by default
            follow_utils.follow(request.user, report)
            # notify new report
            notify_new_report(report, request.user)
                
        else:
            errors.update(video_formset.errors)
    else:
        errors.update(report_form.errors)
                     
    #except:
    #    errors['general'] = u'Hubo un error. Por favor inténtelo nuevamente.'
     
    # dajax response
    if errors:
        dajax.add_data({'errors': errors, 'form_id': form_data['form_id'] },'Datea.report.form_errors')
    else:
        # update activity stream
        dajax.assign('#my-profile-stream-content','innerHTML', render_activity_stream_content(request.user))
        # update report data
        report_data = {
                int(report.id): {
                    'map_data': report.get_map_data()
                }
            }
        dajax.add_data({'reports': report_data}, 'Datea.report.update_report')
        
        form_data = {
            'form_id': form_data['form_id'],
            'action': 'create',
            'success_html': render_to_string("datea_report/_report_create_success.html", {'report': report, 'view_in_map': False}, context_instance=RequestContext(request)),
        }
        dajax.add_data(form_data, 'Datea.report.form_success')

    dajax.script('Datea.hide_body_loading();')       
    return dajax.json()


@login_required
@dajaxice_register
def edit_report(request, report_id):
    dajax = Dajax()
    report = Report.objects.get(pk=report_id)
    active_cat = report.root_category()
    env_data  = report.environment.build_environment_data()
    
    if report.can_edit(request.user):
        report_form = ReportFormInsideEnv(instance=report)
        report_video_formset = ReportVideoFormSet(instance=report)
        tpl_vars = {
            'report': report,
            'environment': report.environment,
            'environment_data': env_data,
            'active_category': active_cat,
            'report_form': report_form,
            'report_video_formset': report_video_formset,    
        }
        form_html = render_to_string('datea_report/_report_edit_form.html', tpl_vars, context_instance=RequestContext(request))
        data = {'report_id': int(report.id), 'edit_form': form_html, 'maincat_id': int(active_cat.id)}
        dajax.add_data(data, 'Datea.report.init_edit')
    else:
        dajax.script("alert('error');")
    
    dajax.script('Datea.hide_body_loading();')
    return dajax.json()


@login_required
@dajaxice_register
def update_report(request, form_data):
    
    mode = 'frontend'
    if 'inbox-edit-report' in form_data['form_id']:
        mode = 'inbox'
    
    dajax = Dajax()
    errors = {}
    
    report = Report.objects.get(pk=form_data['report_id'])
    
    if report.can_edit(request.user):
        
        if mode == 'frontend':
            edit_report_form = ReportFormInsideEnv(form_data, instance=report)
        else:
            edit_report_form = ReportEnvAdminForm(form_data, instance=report)
        
        if edit_report_form.is_valid():
            
            report = edit_report_form.save(commit=False)
            edit_video_formset = ReportVideoFormSet(form_data, instance=report)
            if edit_video_formset.is_valid():
                
                report.author = request.user # asegurarse de quien es el autor
                report.site = Site.objects.get_current() # lo mismo para site environment
                
                report.save()
                edit_report_form.save_m2m()
                edit_video_formset.save()
                    
            else:
                errors.update(edit_video_formset.errors)
        else:
            errors.update(edit_report_form.errors)
                     
    else:
        errors['general'] = u'Hubo un error. Por favor inténtelo nuevamente.'
     
    # dajax response
    if errors:
        if mode == 'frontend':
            dajax.add_data({'errors': errors, 'form_id': form_data['form_id'] },'Datea.report.form_errors')
        else:
            dajax.add_data({'errors': errors, 'form_id': form_data['form_id'] },'Datea.inbox.submit_report_error')
    else:
        # update activity stream
        # dajax.assign('#my-profile-stream-content','innerHTML', render_activity_stream_content(request.user))
        # update report data
        if mode == 'frontend':
            report_data = { int(report.id): { 'map_data': report.get_map_data() } }
            dajax.add_data({'reports': report_data}, 'Datea.report.update_report')            
            # UPDATE REPORT FORM
            form_data = {
                'report_id': int(report.id),
                'form_id': form_data['form_id'],
                'report_nav': report.get_nav_url(),
                'maincat_id': int(report.root_category().id),
                'new_report_form':render_new_report_form(request, report.environment, report.root_category()),
            }
            dajax.add_data(form_data, 'Datea.report.edit_form_success')
        else:
            dajax.add_data(int(report.id), 'Datea.inbox.submit_report_success')

    dajax.script('Datea.hide_body_loading();')       
    return dajax.json()

      
        
def render_new_report_form(request, environment, active_category):
    new_report = Report(author=request.user, site=Site.objects.get_current(), environment=environment)
    tpl_vars = {
            'active_category': active_category,
            'environment': environment,
            'environment_data': environment.build_environment_data(),
            'report_form': ReportFormInsideEnv(instance=new_report),
            'report_video_formset': ReportVideoFormSet(instance=new_report)
        }
    return render_to_string("datea_report/_report_create_form.html", tpl_vars, context_instance=RequestContext(request))



@login_required
@dajaxice_register
def reload_new_report_form(request, env_slug, cat_id):
    dajax = Dajax()
    environment = ReportEnvironment.objects.get(slug=env_slug)
    category = Category.objects.get(pk=cat_id)
    data = {
        'new_report_form': render_new_report_form(request, environment, category),
    }
    dajax.add_data(data, 'Datea.report.reload_new_report_form_success')
    dajax.script('Datea.hide_body_loading();')
    return dajax.json()



@login_required
@dajaxice_register
def cancel_edit_report(request, data):
    dajax = Dajax()
    report = Report.objects.get(pk=data['report_id']);
    data = {
        'form_id': data['form_id'],
        'report_id': data['report_id'],
        'report_nav': report.get_nav_url(),
        'maincat_id': int(report.root_category().id),
        'new_report_form': render_new_report_form(request, report.environment, report.root_category()),
    }
    dajax.add_data(data, 'Datea.report.cancel_edit_success')
    dajax.script('Datea.hide_body_loading();')       
    return dajax.json()
    
#+++++++++++++++++++++++++++++
# ENVIRONMENT NAVIGATION AJAX

@dajaxice_register
def get_report_teaser_list_page(request, tab_id, page_num, env_slug, main_cat_id, sub_cat_ids=[]):
    
    dajax = Dajax()
    current_site = Site.objects.get_current()
    current_environment = ReportEnvironment.objects.get(slug=env_slug, sites=current_site)
    active_category = Category.objects.get(pk=int(main_cat_id))
    reports = get_report_object_list(current_environment, current_site, [main_cat_id] + sub_cat_ids)
    if tab_id == 'tab-voted-reports':
        report_page = get_report_page(reports.filter(vote_count__gt=0).order_by('-vote_count','-created'), page_num)
        tab_prefix = 'voted/page/'
    elif tab_id == 'tab-commented-reports':
        report_page = get_report_page(reports.filter(comment_count__gt=0).order_by('-comment_count','-created'), page_num)
        tab_prefix = 'commented/page/'
    else:
        report_page = get_report_page(reports.order_by('-created'), page_num)
        tab_prefix = 'page/'
    
    tpl_vars = {
            'report_list_page': report_page,
            'base_page_url': reverse('reports_list', args=[current_environment.slug, active_category.slug]),
            'tab_prefix': tab_prefix,
            'active_category': active_category,
            }
    
    report_page_html = render_to_string("datea_report/_report_list_page.html", tpl_vars, context_instance= RequestContext(request))
    
    dajax.assign('#'+tab_id+'-content', 'innerHTML', report_page_html)
    dajax.script('Datea.hide_loading("#reports-tab-content .left");')
    return dajax.json()


@dajaxice_register
def get_report_detail(request, report_id):
    
    dajax = Dajax()
    try:
        report = Report.objects.get(pk=report_id)
    except:
        report = False
    
    tpl_vars =  {
        'report': report
                 }
    tpl_vars['replies'] = report.replies.all().order_by('created')
    
    html = render_to_string("datea_report/_report_full.html", tpl_vars, context_instance=RequestContext(request))
    dajax.assign('#report-detail-content', 'innerHTML', html)
    dajax.script('Datea.hide_loading("#reports-tab-content .left");')
    dajax.script('Datea.share.init_add_this();');
    return dajax.json()


@dajaxice_register
def reload_maincat(request, actions):
    
    # GET REPORT OBJECTS
    dajax = Dajax()
    current_site = Site.objects.get_current()
    current_environment = ReportEnvironment.objects.get(slug=actions['env_slug'], sites=current_site)
    active_category = Category.objects.get(slug=actions['reload_maincat'])
    
    report_objects = get_report_object_list(current_environment, current_site, [active_category.id])
    
    # REBUILD REPORT DATA
    report_data = build_report_data(report_objects)
    ctx = RequestContext(request)
    dajax.add_data(report_data, 'Datea.report.rebuild_map')
    
    # REPORT PAGES: MOST RECENT, MOST VOTED, MOST COMMENTED
    recent_page = 1
    voted_page = 1
    commented_page = 1
    subtab = 'recent'
    
    if 'subtab' in actions and actions['subtab'] != '':
        subtab = actions['subtab']
        
    if 'page' in actions and 'subtab' in actions:
        if actions['subtab'] == '' or actions['subtab'] == 'recent':
            recent_page = actions['page']
        elif actions['subtab'] == 'voted':
            voted_page = actions['page']
        elif actions['subtab'] == 'commented':
            commented_page = actions['page']
    
    tpl_vars = {
            'reports_most_recent': get_report_page(report_objects.order_by('-created'), recent_page),
            'reports_most_voted': get_report_page(report_objects.filter(vote_count__gt=0).order_by('-vote_count','-created'), voted_page),
            'reports_most_commented': get_report_page(report_objects.filter(comment_count__gt=0).order_by('-comment_count','-created'), commented_page),
            'active_category': active_category,
            'environment': current_environment,
            'report_list_tab': subtab,
    }
    pages_html = render_to_string('datea_report/_report_list_pages.html', tpl_vars, context_instance=ctx)
    dajax.assign('#report-pages-container', 'innerHTML', pages_html)
    
    # RELOAD NEW REPORT FORM (later)
    reload_form_data = {'new_report_form': render_new_report_form(request, current_environment, active_category)}
    dajax.add_data(reload_form_data, 'Datea.report.reload_new_report_form_success')
    
    # LOAD REPORT, IF NECESSARY
    if 'load_report' in actions:
        try:
            report = Report.objects.get(pk=actions['load_report'])
            html = render_to_string("datea_report/_report_full.html", {'report': report }, ctx)
            dajax.assign('#report-detail-content', 'innerHTML', html)
            dajax.script('Datea.share.init_add_this();');
        except:
            pass
     
    dajax.add_data(actions, 'Datea.report.reports_tab_actions_success')    
    dajax.script('Datea.hide_body_loading();')
    return dajax.json()
    
    
@login_required
@dajaxice_register
def edit_change_maincat(request, cat_id, env_slug): 
    dajax = Dajax()
    env = ReportEnvironment.objects.get(slug=env_slug)
    env_data = env.build_environment_data()
    maincat = Category.objects.get(pk=cat_id)
    tpl_vars = {
                'environment': env,
                'environment_data': env_data,
                'active_category': maincat,
                }
    select_html = render_to_string('datea_report/_subcat_select.html', tpl_vars)
    dajax.assign('#report-subcat-select', 'innerHTML', select_html)
    maincat_html = render_to_string('datea_report/_report_form_maincat.html', tpl_vars)
    dajax.assign('#report-maincat-select', 'innerHTML', maincat_html)
    dajax.script('Datea.hide_loading("#new-report-tab-content .left");')
    return dajax.json()
        
        
    
    
    
    
    
    
    
    
    
    
    
    