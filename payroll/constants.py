from datetime import datetime


PAYROLL_YEARS = [(year, year) for year in range(datetime.now().year, datetime.now().year + 10)]

month_str = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY',
             'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
             'NOVEMBER', 'DECEMBER']

MONTHS = [(month_str[month-1], month_str[month-1]) for month in range(1, 13)]

OPEN_OR_CLOSED = (
    ('OPEN', 'Open'),
    ('CLOSED', 'Closed')
)
