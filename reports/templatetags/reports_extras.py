from django import template

register = template.Library()


@register.filter
def obj_type(obj):
    return type(obj)


@register.filter
def get_distinct_employee_set(processors):
    employees_in_period = []
    for process in processors:
        employees_in_period.append(process.employee)

    return list(set(employees_in_period))


@register.filter
def total_amount(processors):
    total = 0
    for inst in processors:
        total += inst.amount
    return total
