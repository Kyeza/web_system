from django_celery_results.models import TaskResult

from payroll.models import PayrollPeriod
from reports.tasks import update_or_create_user_summary_report, initialize_report_generation
from users.models import PayrollProcessors


def run_report_gen():
    for period in PayrollPeriod.objects.filter(status='CLOSED').iterator():
        data = PayrollProcessors.objects.filter(payroll_period_id=period.id).all()

        employees_in_period = set()
        for d in data:
            employees_in_period.add(d.employee)

        reports_emps = []
        for employee in employees_in_period:
            user_info = {
                'employee_id': employee.pk,
                'analysis': employee.agresso_number,
                'staff_full_name': employee.user.get_full_name(),
                'job_title': employee.job_title.job_title,
                'basic_salary': employee.gross_salary,
                'payment_method': employee.payment_method,
                'duty_station': employee.duty_station.duty_station,
                'social_security_number': employee.social_security_number,
                'tin_number': employee.tin_number
            }

            period_info = {
                'period_id': period.id,
                'period': period.created_on.strftime('%B, %Y')
            }

            report = employee.report.filter(payroll_period_id=period.id).values('gross_earning', 'net_pay',
                                                                                'total_deductions').first()

            # create or update user reports
            update_or_create_user_summary_report(f'{period.payroll_key}S{employee.pk}', user_info, report['net_pay'],
                                                 report['total_deductions'], report['gross_earning'], period_info)
            reports_emps.append(employee.pk)

        result = initialize_report_generation.delay(period.id, reports_emps)

        cont = True
        while cont:
            if result.status == 'SUCCESS':
                cont = False
            elif result.status == 'FAILURE' and result.traceback is not None:
                return result
            else:
                cont = True
