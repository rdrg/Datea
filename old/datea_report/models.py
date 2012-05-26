from django.contrib.gis.db import models
from sorl.thumbnail import ImageField

from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel
from mptt.fields import TreeNodeChoiceField, TreeForeignKey, TreeOneToOneField, TreeManyToManyField
from mptt.utils import tree_item_iterator 

from olwidget.widgets import EditableMap
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from datea_images.fields import DateaImageM2MField

from django.utils import simplejson
from django.template.defaultfilters import slugify
from utils import truncate_chars
from django.utils.translation import ugettext_lazy as _

from django.template.loader import render_to_string
from django.utils.dateformat import format as date_format

from rulez import registry as rulez_registry


def get_current_site_id():
    site = Site.objects.get_current()
    return site.id
def get_current_site_id_list():
    site = Site.objects.get_current()
    return [site.id]


class Report(models.Model):
    
    author = models.ForeignKey(User, related_name="reports")
    
    # timestamps
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    # status, published
    published = models.BooleanField(default=True)
    #status
    status_choices = ((u'new',u'nuevo'), (u'reviewed', u'atendido'), (u'solved', u'solucionado'))
    status = models.CharField(max_length=15, choices=status_choices, default="new")
    
    # content
    title = models.CharField(max_length=100, blank=True, null=True)
    
    problem = models.TextField(verbose_name=_("Problem"))
    solution = models.TextField(blank=True, null=True, verbose_name=_("Solution"))
    
    # location
    position = models.PointField(blank=True, null=True, spatial_index=False)
    location_description = models.TextField(blank=True, null=True, verbose_name=_("Location description"))
    
    street = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Street"))
    
    zone = models.ForeignKey('Zone', null=True, blank=True, default=None, related_name="reports") 
    category = TreeManyToManyField('Category', null=True, blank=True, default=None, related_name="reports")
    environment = models.ForeignKey('ReportEnvironment', related_name="reports")
    
    # stats
    vote_count = models.IntegerField(default=0, blank=True, null=True)
    comment_count = models.IntegerField(default=0,blank=True, null=True)
    follow_count = models.IntegerField(default=0, blank=True, null=True)
    reply_count = models.IntegerField(default=0, blank=True, null=True)
    
    objects = models.GeoManager()
    # site
    site = models.ForeignKey(Site, default=get_current_site_id)
    on_site = CurrentSiteManager()
    
    images = DateaImageM2MField(null=True, blank=True, max_images=3)
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.title == None or self.title == '':
            title = ''
            if (self.author_id != None):
                title += self.author.username+': '
            title += self.problem
            self.title = truncate_chars(title,100)
        super(Report, self).save(*args, **kwargs)
        
    def root_category(self):
        cat = None
        for cat in self.category.all():
            if cat.is_root_node():
                break
        if cat != None: 
            return cat
        else:
            return Category.objects.get(reports__pk=self.pk, parent=None)
            
    def leaf_category(self):
        cat = None
        for cat in self.category.all():
            if cat.is_leaf_node():
                break
        if cat != None:
            return cat
        else:
            return Category.objects.exclude(parent=None).get(reports__pk=self.pk)
            
    @models.permalink
    def get_absolute_url(self):
        return ('report_detail', (), {
                'env_slug': self.environment.slug,
                'cat_slug': self.root_category().slug,
                'report_id': str(self.id)
                })
    
    # jquery address url   
    def get_nav_url(self):
        return 'reports/'+self.root_category().slug+'/'+str(self.id)
    
    def get_full_url(self):
        site = Site.objects.get_current()
        return 'http://'+str(site)+self.get_absolute_url()
    
    def get_map_data(self, with_id=False, complete=False):
        data = {
            't': self.title, 
            'c': int(self.leaf_category().id),
            'd': int(date_format(self.created, 'U')),
            'html': render_to_string('datea_report/_report_popup.html', {'report': self}),
            's': self.status[0],
            }
        if self.position:
            data['wkt'] = self.position.wkt
        if with_id:
            data['id'] = int(self.pk)
        if complete:
            data['mc'] = int(self.root_category().id)
            if self.zone:
                data['z'] = int(self.zone.id)
            
        return data
    
    def can_edit(self, user_inst):
        if self.author == user_inst or user_inst.is_staff:
            return True
        elif self.environment.admin_group in user_inst.groups.all():
            return True
        return False
    
rulez_registry.register('can_edit', Report)
     
     
class ReportVideo(models.Model):
    video = models.CharField(max_length=255)
    report = models.ForeignKey('Report', related_name="video")
    objects = models.GeoManager()
    
    
class Zone(models.Model):
    title = models.CharField(max_length=100, verbose_name="Nombre")
    content = models.TextField()
    
    active = models.BooleanField(default=True)
    
    # GEO
    center = models.PointField(blank=True, null=True, spatial_index=False)
    boundary = models.PolygonField()
    objects = models.GeoManager()
    
    environment = models.ForeignKey('ReportEnvironment', null=True, blank=True, default=None, related_name="zones")
    
    # Site specific
    #sites = models.ManyToManyField(Site, default=[Site.objects.get_current().id])
    #on_site = CurrentSiteManager()
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.center == None:
            self.center = self.boundary.centroid
            self.center.srid = self.boundary.get_srid()
        super(Zone, self).save(*args, **kwargs)
        
    def build_data(self):
        return {
                'id': self.pk,
                'title': self.title,
                'desc': self.content,
                'center': self.center.get_coords(),
                'center_srid': self.center.get_srid(),
                'boundary': self.boundary.coords,
                'boundary_srid': self.boundary.get_srid()
                }
  
  
    
class Category(MPTTModel):
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, blank=True, null=True)
    description = models.TextField(max_length=500)
    
    active = models.BooleanField(default=True)
     
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    color = models.CharField(max_length=7, default='#cccccc')
    image = ImageField(upload_to="category/images", blank=True, null=True)
    image_off = ImageField(upload_to="category/images", blank=True, null=True)
    marker_image = models.ImageField(upload_to='category/markers', blank=True, null=True)
    
    sites = models.ManyToManyField(Site, default=get_current_site_id_list)
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def save(self, *args, **kwargs):
        if self.slug == 'slug' or self.slug == None or self.slug == '':
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    
class ReportEnvironment(models.Model):
    
    admin_group = models.ForeignKey(Group, blank=True, null=True)
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=15)
    
    welcome_message = models.TextField(blank=True, null=True)
    report_success_message = models.TextField(blank=True, null=True)
    
    active = models.BooleanField()
    
    # ZONES
    #zones = models.ManyToManyField(Zone, blank=True, null=True, default=None)
    
    # CATEGORIES
    categories = TreeManyToManyField(Category, blank=True, null=True, default=None)
    
    # GEO:
    center = models.PointField(blank=True, null=True, spatial_index=False)
    boundary = models.PolygonField(blank=True, null=True, spatial_index=False)
    objects = models.GeoManager()
    
    # SITE SPECIFIC
    sites = models.ManyToManyField(Site, default=get_current_site_id_list)
    on_site = CurrentSiteManager()
    
    class Meta:
        verbose_name = "Report Environment"
        verbose_name_plural = 'Report Environments'
        permissions = (
                       ("can_create_report_environment", "Can create Report Evironment"),
                       ("can_edit_report_environment", "Can edit Report Environment"),
                       ("can_delete_report_environment", "Can delete Report Environment"),
        )
        #unique_together = ('sites', 'slug')
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.center == None and self.boundary != None:
            self.center = self.boundary.centroid
            self.center.srid = self.boundary.get_srid()
        super(ReportEnvironment, self).save(*args, **kwargs)
        
        
    def build_categories(self):
        
        root_items = self.categories.filter(level=0, active=True).order_by('tree_id')
        cats = {}
        for ritem in root_items:
            rcat_id = int(ritem.id)
            cats[rcat_id] = {
                    'id': rcat_id,
                    'name': ritem.name,
                    'slug': ritem.slug,
                    'desc': ritem.description,
                    'color': ritem.color, 
                }
            if ritem.image:
                cats[rcat_id]['image'] = ritem.image.name
            if ritem.image_off:
                cats[rcat_id]['image_off'] = ritem.image_off.name    
                
            if ritem.marker_image:
                cats[rcat_id]['marker'] = {
                        'src': ritem.marker_image.url,
                        'w': ritem.marker_image.width,
                        'h': ritem.marker_image.height
                }
                
            children = ritem.get_children()
            if len(children) > 0:
                cats[rcat_id]['children'] = {}
                for citem in children:
                    ccat_id = int(citem.id)
                    cats[rcat_id]['children'][ccat_id] = {
                    'id': ccat_id,
                    'name': citem.name,
                    'slug': citem.slug,
                    'desc': citem.description,
                    'color': citem.color, 
                        }
                    if citem.image:
                        cats[rcat_id]['children'][ccat_id]['image'] = citem.image.name
                    if citem.image_off:
                        cats[rcat_id]['children'][ccat_id]['image_off'] = citem.image_off.name    
                        
                    if citem.marker_image:
                        cats[rcat_id]['children'][ccat_id]['marker'] = {
                                'src': citem.marker_image.url,
                                'w': citem.marker_image.width,
                                'h': citem.marker_image.height
                        }
        return cats
                
        
        items = self.categories.filter(active=True)
        if len(items) == 0: 
            return False
        
        cats = {}
        levels = [cats]
        iter = tree_item_iterator(items)
        
        for item, data in iter:
                            
            this_level = levels[-1]
            cat_id = int(item.pk)
            this_level[cat_id] = {
                    'id': cat_id,
                    'name': item.name,
                    'slug': item.slug,
                    'desc': item.description,
                    'color': item.color, 
                }
            if item.image:
                this_level[cat_id]['image'] = item.image.name
            if item.image_off:
                this_level[cat_id]['image_off'] = item.image_off.name    
                
            if item.marker_image:
                this_level[cat_id]['marker'] = {
                        'src': item.marker_image.url,
                        'w': item.marker_image.width,
                        'h': item.marker_image.height
                }
            
            if item.is_leaf_node() == False:
                this_level[cat_id]['children'] = {}
                this_level = this_level[cat_id]['children']
                levels.append(this_level)
            if len(data['closed_levels']) > 0:
                levels = levels[:-len(data['closed_levels'])]   
        return cats
                       
    def build_environment_data(self):
        data =  {
                 'name': self.name,
                 'slug': self.slug,
                 'center': self.center.get_coords() or '',
                 'center_srid': self.center.get_srid(),
                 'boundary': self.boundary.coords or '',
                 'boundary_srid': self.boundary.get_srid(),
                 }
        
        if self.zones != None:
            items = self.zones.filter(active=True)
            if len(items) > 0:
                data['zones'] = {}
                for z in items:
                    data['zones'][z.pk] = z.build_data()
        if self.categories != None:
            data['categories'] = self.build_categories()
        return data
    
    def get_json_environment(self):
        data = self.build_environment_data()
        return simplejson.dumps(data)
       
            
            