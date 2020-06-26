from rest_framework import viewsets

from reports.models import ExTraSummaryReportInfo
from reports.serializers import SummaryReportSerializer


class SummaryReportViewSet(viewsets.ModelViewSet):
    queryset = ExTraSummaryReportInfo.objects.all()
    serializer_class = SummaryReportSerializer
