from django.utils.html import strip_tags
from django.utils.text import truncate_words

def truncate_chars(s, max_chars, ellipsis='...'):
    
    if len(s) <= max_chars:
        return s
    max_chars -= len(ellipsis)
    s = strip_tags(s)
    words = len(s[:max_chars].split(' ')) -1
    return truncate_words(s, words, ellipsis)
  
  
import re
tag_end_re = re.compile(r'(\w+)[^>]*>')
entity_end_re = re.compile(r'(\w+;)')  
    
def truncate_html_chars(string, length, ellipsis='...'):
    """Truncate HTML string, preserving tag structure and character entities."""
    length = int(length)
    output_length = 0
    i = 0
    pending_close_tags = {}
    
    while output_length < length and i < len(string):
        c = string[i]

        if c == '<':
            # probably some kind of tag
            if i in pending_close_tags:
                # just pop and skip if it's closing tag we already knew about
                i += len(pending_close_tags.pop(i))
            else:
                # else maybe add tag
                i += 1
                match = tag_end_re.match(string[i:])
                if match:
                    tag = match.groups()[0]
                    i += match.end()
  
                    # save the end tag for possible later use if there is one
                    match = re.search(r'(</' + tag + '[^>]*>)', string[i:], re.IGNORECASE)
                    if match:
                        pending_close_tags[i + match.start()] = match.groups()[0]
                else:
                    output_length += 1 # some kind of garbage, but count it in
                    
        elif c == '&':
            # possible character entity, we need to skip it
            i += 1
            match = entity_end_re.match(string[i:])
            if match:
                i += match.end()

            # this is either a weird character or just '&', both count as 1
            output_length += 1
        else:
            # plain old characters
            
            skip_to = string.find('<', i, i + length)
            if skip_to == -1:
                skip_to = string.find('&', i, i + length)
            if skip_to == -1:
                skip_to = i + length
                
            # clamp
            delta = min(skip_to - i,
                        length - output_length,
                        len(string) - i)

            output_length += delta
            i += delta
                        
    output = [string[:i]]
    if output_length == length:
        output.append(ellipsis)

    for k in sorted(pending_close_tags.keys()):
        output.append(pending_close_tags[k])

    return "".join(output)


import svgwrite, math
from django.template.defaultfilters import slugify
from django.conf import settings
import os.path
from subprocess import call

def get_svg_circle(radius, color):
    radius = int(radius)
    filename = slugify(str(radius)+str(color))
    media_path = 'datea/img/circles'
    root_path = os.path.join(settings.MEDIA_ROOT, media_path)
    svg_filename = filename+'.svg'
    png_filename = filename+'.png'
    
    if os.path.exists(os.path.join(root_path, png_filename)):
        return os.path.join(root_path, png_filename)
    
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    
    size = radius * 2
    border = 3
    dwg = svgwrite.Drawing(filename = os.path.join(root_path, svg_filename), size = (str(size)+"px", str(size)+"px"), fill_opacity="0")
    
    circle = svgwrite.shapes.Circle(center=(radius, radius), r=radius-border, stroke_width=border, stroke_opacity="0.5", stroke='#'+color, fill='#'+color, fill_opacity="1")
    dwg.add( circle )
    
    dwg.save()
    call('convert -background none '+os.path.join(root_path, svg_filename)+' '+os.path.join(root_path, png_filename), shell=True)
    return os.path.join(root_path, png_filename)
    

def get_svg_pie_cluster(radius, values, colors):
    
    radius = int(radius)
    values = map(int,values)
    
    filename = slugify(str(radius)+"".join(map(str,values))+"".join(colors))
    media_path = 'datea/img/pie_clusters'
    
    root_path = os.path.join(settings.MEDIA_ROOT, media_path)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
     
    svg_filename = filename+'.svg'
    png_filename = filename+'.png' 
        
    if os.path.exists(os.path.join(root_path, png_filename)):
        return os.path.join(root_path, png_filename)
    
    total = sum(map(int,values))
    
    label_txt = str(total)
    if len(label_txt) == 1:
        f_size = '9px'
        bg_radius = 6
        y_offset = 3
        x_offset = 0
    elif len(label_txt) == 2:
        f_size = '10px'
        bg_radius = 8
        y_offset = 4
        x_offset = 0 
    else:
        f_size = '11px'
        bg_radius = 12
        y_offset = 4
        x_offset = 0  
    
    size = radius * 2
    dwg = svgwrite.Drawing(filename = os.path.join(root_path, svg_filename), size = (str(size)+"px", str(size)+"px"), fill_opacity="0")
    
    border_ratio = 0.4
    border_width = radius * border_ratio
    fill_radius = radius * (1 - border_ratio)
    border_radius = fill_radius + (border_width / 2.0)
    
    if fill_radius < bg_radius + 2:
        fill_radius = bg_radius + 2;
        border_radius = radius - fill_radius
        
    
    
    center_x = radius
    center_y = radius 
    
    dospi = math.pi * 2
    
    angulo = 0
    
    last_f_x = fill_radius
    last_f_y = 0
    last_b_x = border_radius
    last_b_y = 0
    
    #borde blanco
    #border = svgwrite.shapes.Circle(center=(center_x, center_y), r=radius+1, stroke_width=border_width, stroke_opacity="0.5", stroke="white", fill_opacity="0", style="z-index:0")
    #dwg.add( border )
    
    # create pie if more than one category
    if len(values) > 1:
        for i, val in enumerate(values):
            arc = 0
            alpha = (val / float(total)) * dospi
            if alpha > math.pi:
                arc = 1
        
            angulo += alpha
            
            next_f_x = math.cos(angulo) * fill_radius 
            next_f_y = math.sin(angulo) * fill_radius
            next_b_x = math.cos(angulo) * border_radius
            next_b_y = math.sin(angulo) * border_radius  
            
            path = svgwrite.path.Path(fill='#'+colors[i], fill_opacity="1", stroke_width=0, style="z-index: 2")
            path.push('M '+str(center_x)+','+str(center_y)) 
            path.push('l '+str(last_f_x)+','+str(-last_f_y)) 
            path.push('a '+str(fill_radius)+','+str(fill_radius)+' 0 '+str(arc)+', 0 '+str(next_f_x - last_f_x)+','+str(-(next_f_y - last_f_y))+' z')
            
            border_path = svgwrite.path.Path(stroke='#'+colors[i], stroke_opacity=0.6, fill_opacity=0, stroke_width=border_width, style="z-index: 1")
            border_path.push('M '+str(center_x)+','+str(center_y))
            border_path.push('m '+str(last_b_x)+','+str(-last_b_y))
            border_path.push('a '+str(border_radius)+','+str(border_radius)+' 0 '+str(arc)+', 0 '+str(next_b_x - last_b_x)+','+str(-(next_b_y - last_b_y)))
        
            dwg.add( path )
            dwg.add( border_path )
            
            last_f_x = next_f_x
            last_f_y = next_f_y
            last_b_x = next_b_x
            last_b_y = next_b_y
            
    # create circle for single category
    else:
        circ = svgwrite.shapes.Circle(center=(center_x, center_y), r=fill_radius, stroke_width=border_width *2, fill='#'+colors[0], fill_opacity="1", stroke="#"+colors[0], stroke_opacity=0.6, style="z-index: 2")
        dwg.add( circ ) 
    
    label = svgwrite.text.Text(str(total), insert=(center_x + x_offset, center_y + y_offset), fill='#555555', text_anchor="middle", style="font-family: Helvetica; font-size: "+f_size+"; font-weight: 700; z-index: 4", fill_opacity="1")
    label_bg = svgwrite.shapes.Circle(center=(center_x, center_y), r=bg_radius, fill="#efefef", fill_opacity="0.9", style="z-index: 3")
    
    dwg.add( label_bg )
    dwg.add( label )
        
    dwg.save()
    call('convert -background none '+os.path.join(root_path, svg_filename)+' '+os.path.join(root_path, png_filename), shell=True)
    return os.path.join(root_path, png_filename)
    
    
    