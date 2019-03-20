from django.contrib import admin

from .models import (EarningDeductionCategory, PayrollCenter, Currency, EarningDeductionType, PayrollPeriod)


admin.site.register(PayrollPeriod)
admin.site.register(PayrollCenter)
admin.site.register(EarningDeductionType)
admin.site.register(EarningDeductionCategory)
admin.site.register(Currency)
