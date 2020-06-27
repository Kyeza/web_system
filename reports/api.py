from rest_framework import viewsets, mixins

from reports.models import ExTraSummaryReportInfo
from reports.pagination import StandardResultsSetPagination
from reports.serializers import SummaryReportSerializer


class SummaryReportViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ExTraSummaryReportInfo.objects.all()
    serializer_class = SummaryReportSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ('payroll_period_id',)
