import json

from django.http import HttpResponse
from django.template.defaultfilters import slugify


def get_image_filename(instance, filename):
    username = instance.user.username
    slug = slugify(username)
    return f'profile_pics/{slug}-{filename}'


def render_to_json(request, data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
        content_type=request.is_ajax() and "application/json" or "text/html"
    )
