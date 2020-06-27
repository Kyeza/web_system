from rest_framework import serializers

from payroll.serializers import EarningOrDeductionSerializer
from users.models import PayrollProcessors


class PayrollProcessorSerializer(serializers.ModelSerializer):
    earning_and_deductions_type = EarningOrDeductionSerializer()

    class Meta:
        model = PayrollProcessors
        fields = [
            'earning_and_deductions_type', 'amount'
        ]
