import json
import logging

from django.contrib import messages
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from users import constants

logger = logging.getLogger('payroll')


def get_image_filename(instance, filename):
    username = instance.user.username
    slug = slugify(username)
    return f'profile_pics/{slug}-{filename}'


def render_to_json(request, data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
        content_type=request.is_ajax() and "application/json" or "text/html"
    )


def display_error_message(err_type, err,  message, request, exception=None):
    error_message = ''
    if err_type == constants.ERROR:
        error_message = messages.error(request, message)
    elif err_type == constants.DEBUG:
        error_message = messages.debug(request, message)
    elif err_type == constants.INFO:
        error_message = messages.info(request, message)

    message = render_to_string('partials/messages.html', {'error_message': error_message})
    logger.error(f"{exception if exception is not None else 'General Exception'}: {err.args}")
    return render_to_json(request, {'status': 'error', 'message': message})
