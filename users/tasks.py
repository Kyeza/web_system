import logging

from celery import shared_task

from payroll.models import PayrollPeriod

logger = logging.getLogger('payroll')


@shared_task
def remove_employee_from_last_payroll_period(payroll_center_id, pk):
    period = PayrollPeriod.objects.filter(payroll_center_id=payroll_center_id).order_by('created_on').last()
    if period is not None and period.status == 'OPEN':
        from users.models import PayrollProcessors
        PayrollProcessors.objects.filter(payroll_period_id=period.id, employee_id=pk).all().delete()
