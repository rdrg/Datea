from django import template
from django.template.defaultfilters import stringfilter
from datea_report.models import Report 

register = template.Library()

@register.filter
def get_item ( item, string ):
    return item.get(string,'')


from datea_report.utils import truncate_html_chars, truncate_chars

@register.filter
@stringfilter
def truncatehtmlchars(s, num):
    """
    Truncates html after a given number of chars  
    Argument: Number of chars to truncate after
    """
    return truncate_html_chars(s, num)

@register.filter
@stringfilter
def truncatechars(s, num):
    """
    Truncates html after a given number of chars  
    Argument: Number of chars to truncate after
    """
    return truncate_chars(s, num)


@register.inclusion_tag('datea_report/_reports_similar.html', takes_context = True)
def get_similar_reports(context, report, num_items):
    user = context['request'].user
    cats = report.category.all()
    reports = Report.objects.filter(category__in=cats).exclude(pk=report.pk, author=user).order_by('-created')[:num_items]
    return {'reports': reports}
    