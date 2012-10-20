from django import template
from datea.datea_blogfeed.feed_functions import get_feed_entries
from time import mktime
from datetime import datetime
from django.conf import settings 

register = template.Library()

@register.inclusion_tag('datea_blogfeed/feed_block.html')
def get_blogfeed_block(num_entries):
    entries = get_feed_entries(num_entries)
    for e in entries:
        e.pubdate_parsed = datetime.fromtimestamp(mktime(e['updated_parsed']))
    return {
            'entries': entries,
            'blog_name': settings.BLOG_NAME,
            'blog_url': settings.BLOG_URL,
            }

