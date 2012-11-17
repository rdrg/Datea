from tastypie import fields
from tastypie.resources import ModelResource
from datea.datea_action.models import DateaAction
from datea.datea_mapping.models import DateaMapping
from tastypie.cache import SimpleCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from datea.datea_follow.models import DateaFollow
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import *
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
from tastypie.utils import trailing_slash
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.gis.geos import Point


class ActionResource(ModelResource):
    
    user = fields.ToOneField('datea.datea_api.profile.UserResource',
            attribute="user", null=False, full=False, readonly=True)
    category = fields.ToOneField('datea.datea_api.category.CategoryResource',
            attribute='category', null=True, full=True, readonly=True)
    #image = fields.ToOneField('datea.datea_api.image.ImageResource', 
    #        attribute='image', full=True, null=True, readonly=True)
    
    def dehydrate(self, bundle):
        bundle.data['url'] = bundle.obj.get_absolute_url()
        bundle.data['type'] = _(bundle.obj.action_type)
        bundle.data['image'] = bundle.obj.get_image_thumb()
        bundle.data['username'] = bundle.obj.user.username
        bundle.data['user_url'] = bundle.obj.user.profile.get_absolute_url()
        bundle.data['is_active'] = bundle.obj.is_active()
        return bundle
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]
        
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query
        q_args = {'published': True}
        if 'q' in request.GET and request.GET['q'] != '':
            q_args['content'] = AutoQuery(request.GET['q'])
        
        params = ['featured', 'category_id', 'category', 'user', 'user_id', 'published']
        for p in params:
            if p in request.GET:
                q_args[p] = request.GET.get(p)
        
        if 'following_user' in request.GET:
            action_ids = [f.object_id for f in DateaFollow.objects.filter(object_type='dateaaction', user__id=int(request.GET['following_user']))]
            q_args['obj_id__in'] = action_ids
            
        # show also one's own unpublished actions
        if request.user.is_authenticated() and 'user_id' in request.GET and int(request.GET['user_id']) == request.user.id:
            del q_args['published']
        
        # make the search query 
        # (using leave action classes because the parent action class somehow doesn't work in haystack) 
        sqs = SearchQuerySet().models(DateaMapping).load_all().filter(**q_args)
        
        order_by = request.GET.get('order_by', '-created')
        if order_by in ['distance', '-distance']:
            if 'lat' in request.GET and 'lng' in request.GET:
                point = Point(float(request.GET['lng']), float(request.GET['lat']))
                sqs = sqs.distance('position', point).order_by(order_by)
            else:
                order_by = '-created'
                
        if order_by not in ['distance', '-distance']:
            sqs = sqs.order_by(order_by)

        if 'limit' in request.GET:
            result_limit = int(request.GET.get('limit',1))
        else:
            result_limit = 15

        print 'result limit: ', result_limit
        paginator = Paginator(sqs, result_limit)

        try:
            print int(request.GET.get('page'))
            page = paginator.page(int(request.GET.get('page',1)))
            #page = paginator.page(2)
        except EmptyPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)


        object_list = {
            'meta': {
                'limit': result_limit,
                'next': page.has_next(),
                'previous': page.has_previous(),
                'total_count': sqs.count(),
                'offset': request.GET.get('page', 0)
            },
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    
    def apply_filters(self, request, applicable_filters):
        if hasattr(request, 'GET') and 'following_user' in request.GET:
            action_ids = [f.object_id for f in DateaFollow.objects.filter(object_type='dateaaction', user__id=int(request.GET['following_user']))]
            applicable_filters['id__in'] = action_ids
            
        return super(ActionResource, self).apply_filters(request, applicable_filters)
    
    
    class Meta:
        queryset = DateaAction.objects.all()
        resource_name = 'action'
        allowed_methods = ['get']
        cache = SimpleCache(timeout=10)
        filtering = {
            'id': ['exact', 'in'],
            'created': ['range', 'gt', 'gte', 'lt', 'lte'],
            'featured': ['exact'],
            'category': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS,
            #'position': ['distance', 'contained','latitude', 'longitude']
        }
        
