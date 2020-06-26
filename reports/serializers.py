from rest_framework import serializers

from reports.models import ExTraSummaryReportInfo


class SummaryReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExTraSummaryReportInfo
        fields = [
            'analysis', 'staff_full_name', 'job_title', 'basic_salary',
            'gross_earning', 'total_deductions', 'net_pay'
        ]
