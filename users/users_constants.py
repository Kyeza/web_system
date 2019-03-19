from django.utils import timezone


GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

MARITAL_STATUS = (
    ('SINGLE', 'Single'),
    ('MARRIED', 'Married'),
    ('SEPARATED', 'Separated'),
    ('DIVORCED', 'Divorced'),
    ('WIDOW', 'Widow')
)

BIRTH_DATE_YEARS_RANGE = [year for year in range(1940, timezone.now().year)]
