from rest_framework import serializers

from payroll.models import EarningDeductionType


class EarningOrDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarningDeductionType
        fields = ['ed_type']
