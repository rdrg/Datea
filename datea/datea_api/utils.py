from tastypie.models import ApiKey

def getOrCreateKey(user):
    try:
        #create a brand new key
        key = ApiKey.objects.create(user=user)
        return key.key
    except:
        #User already has key, so get's retreive it!
        #this fix a postgre error [https://code.djangoproject.com/ticket/10813]
        from django.db import connection 
        connection._rollback()

        key = ApiKey.objects.get(user=user)
        return key.key

def getUserByKey(key):
    try:
        user = ApiKey.objects.get(key=key)
        return user.user
    except ApiKey.DoesNotExist:
        from django.db import connection
        connection._rollback()

        return None
