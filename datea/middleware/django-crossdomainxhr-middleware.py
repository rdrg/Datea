import re

from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers

from django import http

try:
    import datea.settings 
    XS_SHARING_ALLOWED_ORIGINS = datea.settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = datea.settings.XS_SHARING_ALLOWED_METHODS
    XS_SHARING_ALLOWED_HEADERS = datea.settings.XS_SHARING_ALLOWED_HEADERS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
    XS_SHARING_ALLOWED_HEADERS = ['Origin', 'Content-Type', 'Accept', 'Authorization', 'X-CSRFToken']


class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         

        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):
        print request.META
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS ) 
            
            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS ) 

        return response
