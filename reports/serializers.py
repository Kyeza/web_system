from django.db.models import Q
from rest_framework import serializers

from reports.models import ExTraSummaryReportInfo


class SummaryReportSerializer(serializers.HyperlinkedModelSerializer):
    earnings = serializers.SerializerMethodField()
    deductions = serializers.SerializerMethodField()

    class Meta:
        model = ExTraSummaryReportInfo
        fields = [
            'report_id', 'analysis', 'staff_full_name', 'job_title', 'basic_salary', 'earnings',
            'gross_earning', 'deductions', 'total_deductions', 'net_pay'
        ]

    def get_earnings(self, obj):
        earnings = obj.earning_or_deduction.filter(
            Q(earning_and_deductions_type__display_number__gt=1, earning_and_deductions_type__display_number__lt=7))\
            .order_by('earning_and_deductions_type__display_number').select_related('earning_and_deductions_type')\
            .all().values('earning_and_deductions_type__ed_type', 'amount')
        return earnings

    def get_deductions(self, obj):
        deductions = obj.earning_or_deduction.filter(
            Q(earning_and_deductions_type__display_number__gt=6, earning_and_deductions_type__display_number__lt=20))\
            .order_by('earning_and_deductions_type__display_number').select_related('earning_and_deductions_type')\
            .all().values('earning_and_deductions_type__ed_type', 'amount')
        return deductions

    def to_representation(self, instance):
        data = super().to_representation(instance)

        for earning in data['earnings']:
            data[earning['earning_and_deductions_type__ed_type'].lower().replace(' ', '_').replace('.', '_')] = earning['amount']
        del data['earnings']

        for deduction in data['deductions']:
            data[deduction['earning_and_deductions_type__ed_type'].lower().replace(' ', '_')] = deduction['amount']
        del data['deductions']

        return data


