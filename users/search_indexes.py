from haystack import indexes

from .models import Employee


class EmployeeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/Employee_text.txt")
    user = indexes.CharField()
    user_group = indexes.CharField()
    marital_status = indexes.CharField(model_attr='marital_status')
    mobile_number = indexes.IntegerField(model_attr='mobile_number')
    date_of_birth = indexes.DateField(model_attr='date_of_birth')
    sex = indexes.CharField(model_attr='sex')
    id_number = indexes.CharField(model_attr='id_number')
    passport_number = indexes.CharField(model_attr='passport_number')
    residential_address = indexes.CharField(model_attr='residential_address')
    district = indexes.CharField(model_attr='district')
    gross_salary = indexes.DecimalField(model_attr='gross_salary')
    tin_number = indexes.IntegerField(model_attr='tin_number')
    nationality = indexes.CharField()
    grade = indexes.CharField()
    duty_station = indexes.CharField()
    duty_country = indexes.CharField()
    department = indexes.CharField()
    job_title = indexes.CharField()
    contract_type = indexes.CharField()
    appointment_date = indexes.DateField(model_attr='appointment_date')
    social_security = indexes.CharField(model_attr='social_security')
    payroll_center = indexes.CharField()
    bank_1 = indexes.CharField()
    bank_2 = indexes.CharField()
    cost_centre = indexes.CharField()
    first_account_number = indexes.IntegerField(model_attr='first_account_number')
    second_account_number = indexes.IntegerField(model_attr='second_account_number')
    first_bank_percentage = indexes.IntegerField(model_attr='first_bank_percentage')
    second_bank_percentage = indexes.IntegerField(model_attr='second_bank_percentage')
    social_security_number = indexes.CharField(model_attr='social_security_number')
    currency = indexes.CharField()
    kin_full_name = indexes.CharField(model_attr='kin_full_name')
    kin_phone_number = indexes.CharField(model_attr='kin_phone_number')
    kin_email = indexes.CharField(model_attr='kin_email')
    kin_relationship = indexes.CharField()
    dr_ac_code = indexes.CharField(model_attr='dr_ac_code')
    cr_ac_code = indexes.CharField(model_attr='cr_ac_code')
    employment_status = indexes.CharField(model_attr='employment_status')

    def get_model(self):
        return Employee

    def prepare_user(self, obj):
        return [a.get_full_name() for a in obj.user.all()]

    def prepare_user_group(self, obj):
        return [a.group for a in obj.user_group.all()]

    def prepare_nationality(self, obj):
        return [a.country_nationality for a in obj.nationality.all()]

    def prepare_grade(self, obj):
        return [a.grade for a in obj.grade.all()]

    def prepare_duty_station(self, obj):
        return [a.duty_station for a in obj.duty_station.all()]

    def prepare_duty_country(self, obj):
        return [a.country_name for a in obj.duty_country.all()]

    def prepare_department(self, obj):
        return [a.department for a in obj.department.all()]

    def prepare_job_title(self, obj):
        return [a.job for a in obj.job_title.all()]

    def prepare_contract_type(self, obj):
        return [a.get_full_name() for a in obj.contract_type.all()]

    def prepare_payroll_center(self, obj):
        return [a.get_full_name() for a in obj.payroll_center.all()]

    def prepare_bank_1(self, obj):
        return [a.get_full_name() for a in obj.bank_1.all()]

    def prepare_bank_2(self, obj):
        return [a.get_full_name() for a in obj.bank_2.all()]

    def prepare_currency(self, obj):
        return [a.get_full_name() for a in obj.currency.all()]

    def prepare_kin_relationship(self, obj):
        return [a.get_full_name() for a in obj.kin_relationship.all()]

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
#     TODO: Finish up search
