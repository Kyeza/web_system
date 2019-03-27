from django.utils import timezone

GENDER = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
)

EMP_STATUS = (
    ('RECRUIT', 'Recruit'),
    ('APPROVED', 'Approve'),
    ('TERMINATED', 'Terminate'),
    ('REJECTED', 'Reject'),
)

MARITAL_STATUS = (
    ('SINGLE', 'Single'),
    ('MARRIED', 'Married'),
    ('SEPARATED', 'Separated'),
    ('DIVORCED', 'Divorced'),
    ('WIDOWER', 'Widower')
)

YEARS = [year for year in range(1980, timezone.now().year)]
