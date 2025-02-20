import time
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

from django import template
from django.conf import settings
from django.templatetags.static import static as django_static

register = template.Library()


@register.simple_tag
def uncached_static(path):
    static_url = django_static(path)
    if settings.DEBUG:
        parsed_url = urlparse(static_url)
        query_params = parse_qsl(parsed_url.query)
        timestamp = int(time.time())
        query_params.append(("_", str(timestamp)))
        new_query = urlencode(query_params)
        new_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query,
                parsed_url.fragment,
            )
        )
        return new_url
    return static_url
