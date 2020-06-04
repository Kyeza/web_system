from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from payroll.models import PayrollCenter
from support_data.models import Country, Nationality, Organization
from users.models import Employee, Category


class SystemModelTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.country = Country.objects.create(country_name='UGANDA', country_code='UG')
        self.nationality = Nationality.objects.create(country_id=1, country_nationality='UGANDAN')
        self.organization = Organization.objects.create(name='TEST ORG', country_id=1)
        self.user_category = Category.objects.create(name='NATIONAL')
        self.payroll_center = PayrollCenter.objects.create(country_id=1, description='', name='CENTER_NATIONAL',
                                                           organization_id=1, staff_category_id=1)
        self.user = get_user_model().objects.create_user(username='test_user', first_name='test_first',
                                                         middle_name='test_middle', last_name='test_last',
                                                         email='test@email.com', password='test@123')
        self.profile = Employee.objects.create(user=self.user, marital_status='SINGLE', sex='MALE', id_number='SC/123',
                                               gross_salary='2000000', nationality_id=1, payroll_center_id=1)


class UserModelTest(SystemModelTest):

    def test_get_full_name(self):
        """Test if the user model returns all three of user's names"""

        full_name = 'test_first test_middle test_last'

        self.assertEqual(full_name, self.user.get_full_name(),
                         f'expected: {full_name}, actual: {self.user.get_full_name()}')


class EmployeeModelTest(SystemModelTest):

    def test_register_new_employee(self):
        url = reverse('users:new-employee')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
