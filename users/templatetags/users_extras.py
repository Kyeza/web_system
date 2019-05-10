from django import template

import reports
from users.models import User

register = template.Library()


@register.filter
def category(processors, category_id):
    return processors.filter(earning_and_deductions_category=category_id)


@register.filter
def user_data(processors, staff):
    return processors.filter(employee=staff)


@register.filter
def report_key(payroll_period, staff):
    return f'{payroll_period.payroll_key}S{staff.id}'


@register.filter
def extra_info(reports_data, key):
    return reports_data.filter(pk=key)


@register.filter
def user_profile(user):
    try:
        if user:
            return user.employee
        else:
            return None
    except Exception:
        return None
