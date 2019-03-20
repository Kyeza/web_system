from django.utils import timezone


YES_OR_NO_TYPES = (
    ("1", "Yes"),
    ("0", "No")
)

YEARS = [year for year in range(1980, timezone.now().year)]
