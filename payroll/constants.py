from datetime import datetime


PAYROLL_YEARS = [(year, year) for year in range(datetime.now().year, datetime.now().year + 10)]

MONTHS = [(month, month) for month in range(1, 13)]

OPEN_OR_CLOSED = (
    ('OPEN', 'Open'),
    ('CLOSED', 'Closed')
)
