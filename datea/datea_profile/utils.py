from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

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