from datetime import datetime


PAYROLL_YEARS = [(year, year) for year in range(datetime.now().year, datetime.now().year + 10)]

month_str = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY',
             'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
             'NOVEMBER', 'DECEMBER']

MONTHS = [(month_str[month-1], month_str[month-1]) for month in range(1, 13)]

KV_MONTH = {
        'JANUARY': 1,
        'FEBRUARY': 2,
        'MARCH': 3,
        'APRIL': 4,
        'MAY': 5,
        'JUNE': 6,
        'JULY': 7,
        'AUGUST': 8,
        'SEPTEMBER': 9,
        'OCTOBER': 10,
        'NOVEMBER': 11,
        'DECEMBER': 12,
    }