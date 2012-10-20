import feedparser

from django.core.cache import cache
from django.utils.translation import ugettext as _

from django.conf import settings

def get_feed_from_cache():
    if not cache.has_key("blog_feed"):
        feed = feedparser.parse(settings.BLOG_FEED_URL)
        cache.set("blog_feed", feed, settings.BLOG_FEED_CACHE_TIMEOUT)
    return cache.get("blog_feed")


def get_feed_entries(num_entries):
    feed = get_feed_from_cache()
    return feed["entries"][:num_entries]