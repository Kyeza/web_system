from django import template

register = template.Library()


@register.filter
def category(processors, category_id):
    return processors.filter(earning_and_deductions_category=category_id)


@register.filter
def user_data(processors, staff):
    return processors.select_related('employee', 'earning_and_deductions_type', 'employee__user', 'employee__job_title',
                                     'employee__duty_station').filter(employee=staff)


@register.filter
def report_key(payroll_period, staff):
    return f'{payroll_period.payroll_key}S{staff.id_number}'


@register.filter
def extra_info(reports_data, key):
    report = reports_data.get(key=key)
    return report


@register.filter
def user_profile(user):
    try:
        if user:
            return user.employee
        else:
            return None
    except Exception:
        return None
