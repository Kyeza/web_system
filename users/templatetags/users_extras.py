from django import template

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
def extra_info(reports, key):
    return reports.filter(pk=key)
