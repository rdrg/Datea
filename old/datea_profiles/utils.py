
from django.template.defaultfilters import slugify
from social_auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

def make_social_username(username):
    index = 0
    username = slugify(username)
    final_username = username
    
    while True:
        try:
            if index != 0:
                final_username = username+'_'+str(index)
            User.objects.get(username=final_username)
        except User.DoesNotExist:
            break
        else:
            index +=1
    return final_username
    
    
def get_object_page(object_list, page_num=1, items=10):
    paginator = Paginator(object_list, items)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    return page
