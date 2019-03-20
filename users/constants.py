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

YEARS = [year for year in range(1980, timezone.now().year)]
