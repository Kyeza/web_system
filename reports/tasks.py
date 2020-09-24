import datetime
import logging
from typing import Dict, Optional, Any

from celery import shared_task
from celery.task import task
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.timezone import make_aware

from payroll.models import PayrollPeriod
from reports.helpers.mailer import Mailer
from reports.models import ExtraSummaryReportInfo, SocialSecurityReport, TaxationReport, BankReport, LSTReport
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
def initialize_report_generation(payroll_period_id, employees):
    payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)
    period_processes = PayrollProcessors.objects.filter(payroll_period_id=payroll_period_id).all()

    for employee in Employee.objects.filter(pk__in=employees).iterator():
        report_id = f'{payroll_period.payroll_key}S{employee.pk}'

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

        user_bank_info = {}
        if employee.bank_1 is not None:
            user_bank_info['bank_1'] = employee.bank_1.bank
            user_bank_info['branch_name_1'] = employee.bank_1.branch
            user_bank_info['branch_code_1'] = employee.bank_1.branch_code
            user_bank_info['sort_code_1'] = employee.bank_1.sort_code
            user_bank_info['account_number_1'] = employee.first_account_number

        if employee.bank_2 is not None:
            user_bank_info['bank_2'] = employee.bank_2.bank
            user_bank_info['branch_name_2'] = employee.bank_2.branch
            user_bank_info['branch_code_2'] = employee.bank_2.branch_code
            user_bank_info['sort_code_2'] = employee.bank_2.sort_code
            user_bank_info['account_number_2'] = employee.second_account_number

        period_info = {
            'period_id': payroll_period.id,
            'period': payroll_period.created_on.strftime('%B, %Y')
        }

        nssf_5 = nssf_10 = 0
        if employee.social_security == 'YES':
            nssf_10 = period_processes.filter(employee=employee, earning_and_deductions_type_id=31)\
                .values_list('amount').first()
            nssf_5 = period_processes.filter(employee=employee, earning_and_deductions_type_id=32)\
                .values_list('amount').first()

        report = employee.report.filter(payroll_period_id=payroll_period_id).values('gross_earning', 'net_pay').first()

        paye = period_processes.filter(employee=employee, earning_and_deductions_type_id=61)\
            .values_list('amount').first()
        lst = period_processes.filter(employee=employee, earning_and_deductions_type_id=65)\
            .values_list('amount').first()

        update_or_create_user_social_security_report.delay(report_id, user_info, nssf_5[0], nssf_10[0],
                                                           report['gross_earning'], period_info)
        update_or_create_user_taxation_report.delay(report_id, user_info, paye[0], report['gross_earning'], period_info)

        update_or_create_user_bank_report.delay(report_id, user_info, user_bank_info, report['net_pay'], period_info)

        update_or_create_user_lst_report.delay(report_id, user_info, lst[0], report['gross_earning'], period_info)

    return initialize_report_generation.request.id


def update_or_create_user_summary_report(report_id: str, user_info: Dict[str, Optional[Any]], net_pay: float,
                                         total_deductions: float, gross_earning: float,
                                         period_info: Dict[str, Optional[Any]]) -> None:
    report, created = ExtraSummaryReportInfo.objects.get_or_create(report_id=report_id)
    report_count = report.earning_or_deduction.count()

    try:
        logger.info(f"processing summary report for {user_info['staff_full_name']}")
        report.payroll_period_id = period_info['period_id']
        report.employee_id = user_info['employee_id']
        report.analysis = user_info['analysis']
        report.period = make_aware(datetime.datetime.strptime(period_info['period'], "%B, %Y"))
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
        raise

    if report:
        processors_to_report = PayrollProcessors.objects.filter(payroll_period_id=period_info['period_id'],
                                                                employee_id=user_info['employee_id']).all()
        if processors_to_report.count() > report_count:
            for item in processors_to_report.iterator():
                item.summary_report_id = report_id
                item.save()

    if created:
        logger.info(f"created summary report for {user_info['staff_full_name']}")
    else:
        logger.info(f"updated summary report for {user_info['staff_full_name']}")


@shared_task
def update_or_create_user_social_security_report(report_id: str, user_info: Dict[str, Optional[Any]], nssf_5: float,
                                                 nssf_10: float, gross_earning: float,
                                                 period_info: Dict[str, Optional[Any]]) -> None:
    report, created = SocialSecurityReport.objects.get_or_create(report_id=report_id)

    try:
        logger.info(f"processing NSSF report for {user_info['staff_full_name']}")
        report.payroll_period_id = period_info['period_id']
        report.period = make_aware(datetime.datetime.strptime(period_info['period'], "%B, %Y"))
        report.agresso_number = user_info['analysis']
        report.staff_full_name = user_info['staff_full_name']
        report.social_security_number = user_info['social_security_number']
        report.duty_station = user_info['duty_station']
        report.job_title = user_info['job_title']
        report.gross_earning = gross_earning
        report.nssf_5 = nssf_5
        report.nssf_10 = nssf_10
        report.summary_report.report_id = report_id
        report.save()

    except Exception as e:
        logger.error(f"an error occurred while processing NSSF report for {user_info['staff_full_name']}")
        logger.error(e.args)
        raise

    if created:
        logger.info(f"created NSSF report for {user_info['staff_full_name']}")
    else:
        logger.info(f"updated NSSF report for {user_info['staff_full_name']}")


@shared_task
def update_or_create_user_taxation_report(report_id: str, user_info: Dict[str, Optional[Any]], paye: float,
                                          gross_earning: float, period_info: Dict[str, Optional[Any]]) -> None:
    report, created = TaxationReport.objects.get_or_create(report_id=report_id)
    report_count = report.earning_or_deduction.count()

    try:
        logger.info(f"processing PAYE report for {user_info['staff_full_name']}")
        report.payroll_period_id = period_info['period_id']
        report.period = make_aware(datetime.datetime.strptime(period_info['period'], "%B, %Y"))
        report.staff_full_name = user_info['staff_full_name']
        report.tin_number = user_info['tin_number']
        report.gross_earning = gross_earning
        report.paye = paye
        report.summary_report.report_id = report_id
        report.save()

    except Exception as e:
        logger.error(f"an error occurred while processing PAYE report for {user_info['staff_full_name']}")
        logger.error(e.args)
        raise

    if report:
        processors_to_report = PayrollProcessors.objects.filter(payroll_period_id=period_info['period_id'],
                                                                employee_id=user_info['employee_id'],
                                                                earning_and_deductions_category_id=1) \
            .exclude(earning_and_deductions_type_id=19).all()
        if processors_to_report.count() > report_count:
            for item in processors_to_report.iterator():
                item.taxation_report_id = report_id
                item.save()

    if created:
        logger.info(f"created PAYE report for {user_info['staff_full_name']}")
    else:
        logger.info(f"updated PAYE report for {user_info['staff_full_name']}")


@shared_task
def update_or_create_user_bank_report(report_id: str, user_info: Dict[str, Optional[Any]],
                                      user_bank_info: Dict[str, Optional[Any]],
                                      net_pay: float, period_info: Dict[str, Optional[Any]]) -> None:
    if user_info['payment_method'] == 'BANK':
        try:
            bank_1 = user_bank_info['bank_1']
        except KeyError:
            pass
        else:
            report_1, created = BankReport.objects.get_or_create(report_id=f'{report_id}BANK1')
            try:
                logger.info(f"processing BANK report for {user_info['staff_full_name']}")
                report_1.payroll_period_id = period_info['period_id']
                report_1.period = make_aware(datetime.datetime.strptime(period_info['period'], "%B, %Y"))
                report_1.staff_full_name = user_info['staff_full_name']
                report_1.bank = bank_1
                report_1.branch_name = user_bank_info['branch_name_1']
                report_1.branch_code = user_bank_info['branch_code_1']
                report_1.sort_code = user_bank_info['sort_code_1']
                report_1.account_number = user_bank_info['account_number_1']
                report_1.net_pay = net_pay
                report_1.summary_report.report_id = report_id
                report_1.save()

            except Exception as e:
                logger.error(f"an error occurred while processing BANK report for {user_info['staff_full_name']}")
                logger.error(e.args)
                raise

        try:
            bank_2 = user_bank_info['bank_2']
        except KeyError:
            pass
        else:
            report_2, created = BankReport.objects.get_or_create(report_id=f'{report_id}BANK2')
            try:
                logger.info(f"processing BANK report for {user_info['staff_full_name']}")
                report_2.payroll_period_id = period_info['period_id']
                report_2.period = make_aware(datetime.datetime.strptime(period_info['period'], "%B, Y"))
                report_2.staff_full_name = user_info['staff_full_name']
                report_2.bank = bank_2
                report_2.branch_name = user_bank_info['branch_name_2']
                report_2.branch_code = user_bank_info['branch_code_2']
                report_2.sort_code = user_bank_info['sort_code_2']
                report_2.account_number = user_bank_info['account_number_2']
                report_2.net_pay = net_pay
                report_2.summary_report.report_id = report_id
                report_2.save()

            except Exception as e:
                logger.error(f"an error occurred while processing BANK report for {user_info['staff_full_name']}")
                logger.error(e.args)
                raise

            if created:
                logger.info(f"created BANK report for {user_info['staff_full_name']}")
            else:
                logger.info(f"updated BANK report for {user_info['staff_full_name']}")


@shared_task
def update_or_create_user_lst_report(report_id: str, user_info: Dict[str, Optional[Any]], lst,
                                     gross_earning: float, period_info: Dict[str, Optional[Any]]) -> None:
    report, created = LSTReport.objects.get_or_create(report_id=report_id)

    try:
        logger.info(f"processing LST report for {user_info['staff_full_name']}")
        report.payroll_period_id = period_info['period_id']
        report.period = make_aware(datetime.datetime.strptime(period_info['period'], "%B, %Y"))
        report.staff_full_name = user_info['staff_full_name']
        report.duty_station = user_info['duty_station']
        report.gross_earning = gross_earning
        report.lst = lst
        report.summary_report.report_id = report_id
        report.save()

    except Exception as e:
        logger.error(f"an error occurred while processing LST report for {user_info['staff_full_name']}")
        logger.error(e.args)
        raise

    if created:
        logger.info(f"created LST report for {user_info['staff_full_name']}")
    else:
        logger.info(f"updated LST report for {user_info['staff_full_name']}")
