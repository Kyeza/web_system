from django.test import TestCase
from django.urls import reverse

from payroll.models import EarningDeductionType, EarningDeductionCategory
from .views import DutyStationCreate


# Create your tests here.
class TestDutyStationCreationView(TestCase):

    @staticmethod
    def create_ed_type_category(name):
        return EarningDeductionCategory.objects.create(category_name=name)

    @staticmethod
    def create_ed_type(ed_type, description, recurrent, taxable, category):

        return EarningDeductionType.objects.create(ed_type=ed_type, description=description, recurrent=recurrent,
                                                   taxable=taxable, ed_category=category)

    def test_view_creation_form_with_hardship_allowance(self):
        category = self.create_ed_type_category('EARNINGS')
        earning = self.create_ed_type('Hardship allowance', '', 'YES', 'YES', category)
        http_response = self.client.get(reverse('support_data:duty-station-create'))
        template_response = self.client.get(http_response.url)

        self.assertEqual(template_response.status_code, 200)



