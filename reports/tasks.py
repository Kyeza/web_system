import datetime
import logging
from typing import Dict, Optional, Any

from celery import shared_task
from celery.task import task
from django.conf import settings
from django.contrib.auth.models import Group

from reports.helpers.mailer import Mailer
from reports.models import ExTraSummaryReportInfo
from users.models import Employee, PayrollProcessors

logger = logging.getLogger('payroll')


def send_mail(user, expiry, emails, code):
    mailer = Mailer(settings.DEFAULT_FROM_EMAIL)
    subject = 'EMPLOYEE CONTRACT EXPIRED'
    body = ''

    days = 'day' if 0 < expiry.days < 2 else 'days'
    if code == 1:
        body = f'Hello,\n\nThis email is a kind reminder that the contract for {user[0]} {user[1]} expired {expiry.days} {days} ago.'
    elif code == 2:
        body = f'Hello,\n\nThis email is a kind reminder that the contract for {user[0]} {user[1]} will expires in {expiry.days} {days}'
    elif code == 3:
        body = f'Hello,\n\nThis email is a kind reminder that the contract for {user[0]} {user[1]} expires today.'

    body += "\n\n Kindly don't reply to this email as responses to it are not monitored.\n\nRegards"

    mailer.send_messages(subject=subject, body=body, template=None, to_emails=emails)


@task
def contract_expiry_reminder():
    """Task to check user contracts nearing expiry and emails the users and hr group users"""

    logger.info(
        f'Starting contract expiry reminder service on {datetime.datetime.today().strftime("%d %B, %Y, %H:%M")}')

    staff_emails = []
    try:
        group = Group.objects.get(pk=8)
    except Group.DoesNotExist as e:
        logger.debug(f'error occurred while checking contract expiry. error: {e.args}')
    else:
        staff_emails.extend(list(group.user_set.all().values_list('email')))

    all_users = Employee.objects.filter(employment_status='APPROVED').all() \
        .values_list('user__first_name', 'user__last_name', 'contract_expiry', 'user__email')

    if all_users:
        date_now = datetime.date.today()

        for user in all_users.iterator():
            timedelta = user[2] - date_now
            expiry = date_now - user[2]
            if timedelta.days < 0:
                logger.info(f'Contract for {user[0]} {user[1]} expired {expiry.days} days ago')
                staff_emails.append(user[3])
                send_mail(user, expiry, staff_emails, 1)
                staff_emails.remove(user[3])
            elif timedelta.days in range(1, 32):
                logger.info(f'Contract for {user[0]} {user[1]} will expire in {expiry.days} days')
                staff_emails.append(user[3])
                send_mail(user, expiry, staff_emails, 2)
                staff_emails.remove(user[3])
            elif timedelta.days == 0:
                logger.info(f'Contract for {user[0]} {user[1]} expires today')
                staff_emails.append(user[3])
                send_mail(user, expiry, staff_emails, 3)
                staff_emails.remove(user[3])


@shared_task
def update_or_create_user_summary_report(report_id: str, user_info: Dict[str, Optional[Any]], net_pay: float,
                                         total_deductions: float, gross_earning: float,
                                         period_info: Dict[str, Optional[Any]]) -> None:
    report, created = ExTraSummaryReportInfo.objects.get_or_create(report_id=report_id)

    try:
        logger.info(f"processing summary report for {user_info['staff_full_name']}")
        report.payroll_period_id = period_info['period_id']
        report.employee_id = user_info['employee_id']
        report.analysis = user_info['analysis']
        report.period = period_info['period']
        report.staff_full_name = user_info['staff_full_name']
        report.job_title = user_info['job_title']
        report.basic_salary = user_info['basic_salary']
        report.gross_earning = gross_earning
        report.total_deductions = total_deductions
        report.net_pay = net_pay
        report.payment_method = user_info['payment_method']
        report.save()

    except Exception as e:
        logger.error(f"an error occurred while processing summary report for {user_info['staff_full_name']}")
        logger.error(e.args)

    if created:
        logger.info(f"created summary report for {user_info['staff_full_name']}")
        processors_to_report = PayrollProcessors.objects.filter(payroll_period_id=period_info['period_id'],
                                                                employee_id=user_info['employee_id']).all()
        if processors_to_report.exists():
            for item in processors_to_report.iterator():
                item.summary_report_id = report_id
                item.save()
    else:
        logger.info(f"updated summary report for {user_info['staff_full_name']}")
