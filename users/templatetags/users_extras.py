from django import template

register = template.Library()


@register.filter
def category(processors, category_id):
    return processors.filter(earning_and_deductions_category_id=category_id)


@register.filter
def user_data(processors, staff):
    return processors.filter(employee_id=staff.pk)


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
