from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'length'
    offset_query_param = 'start'
    max_limit = 100
