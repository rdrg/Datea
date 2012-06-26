# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from svg2png_map_graphics import get_svg_pie_cluster, get_svg_circle

def redirect_to_hash(request, path):    
    return HttpResponseRedirect('/#/mapping/'+path)

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
