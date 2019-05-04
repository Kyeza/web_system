from django.test import TestCase, Client
from django.urls import reverse


class EmployeeModelTest(TestCase):

    def test_register_new_employee(self):
        response = self.client.get(reverse('users:new-employee'))
        self.assertEqual(response.status_code, 302)

