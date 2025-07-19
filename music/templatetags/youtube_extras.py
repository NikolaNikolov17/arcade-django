from urllib.parse import urlparse, parse_qs

from django import template
import re

register = template.Library()

@register.filter
def youtube_id(value):
    try:
        url_data = urlparse(value)
        query = parse_qs(url_data.query)
        if 'v' in query:
            return query['v'][0]
        elif url_data.path.startswith('/embed/'):
            return url_data.path.split('/')[2]
        elif url_data.netloc == 'youtu.be':
            return url_data.path.lstrip('/')
    except Exception:
        return ''
    return ''