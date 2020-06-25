from django import template
from django.db.models import Q

register = template.Library()


@register.filter
def category(processors, category_id):
    data = processors.filter(earning_and_deductions_category_id=category_id).all()
    return data


@register.filter
def category_display(processors):
    data = list(processors.filter(Q(earning_and_deductions_type__display_number__gt=1,
                                    earning_and_deductions_type__display_number__lt=7) |
                                  Q(earning_and_deductions_type__display_number__gt=6,
                                    earning_and_deductions_type__display_number__lt=20))
                .order_by('earning_and_deductions_type__display_number').select_related('earning_and_deductions_type')
                .all().values_list('earning_and_deductions_type__display_number', 'amount'))

    data = [(list(filter(lambda n: 1 < n[0] < 7, data)), list(filter(lambda n: 6 < n[0] < 20, data)))]
    return data


@register.filter
def user_data(processors, staff):
    data = processors.filter(employee_id=staff.pk).values('amount') \
        .order_by('earning_and_deductions_type__display_number').all()
    return list(data)


@register.filter
def user_data_headings(processors, staff):
    return processors.filter(employee_id=staff.pk).values('earning_and_deductions_type__ed_type') \
        .order_by('earning_and_deductions_type__display_number').all()


@register.filter
def payslip_data(processors, staff):
    return processors.filter(employee_id=staff.pk).values('earning_and_deductions_type__ed_type', 'amount')


@register.filter
def report_key(payroll_period, staff):
    return f'{payroll_period.payroll_key}S{staff.id_number}'


@register.filter
def report(staff, period):
    return staff.report.filter(payroll_period=period).first()


@register.filter
def user_profile(user):
    try:
        if user:
            return user.employee
        else:
            return None
    except Exception:
        return None
