# Generated by Django 2.2 on 2019-04-11 11:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('support_data', '0001_initial'),
        ('auth', '0013_remove_group_group'),
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CostCentre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_centre', models.CharField(max_length=15)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DEA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dea_code', models.CharField(max_length=20)),
                ('dea_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marital_status', models.CharField(choices=[('SINGLE', 'Single'), ('MARRIED', 'Married'), ('SEPARATED', 'Separated'), ('DIVORCED', 'Divorced'), ('WIDOWER', 'Widower')], max_length=9)),
                ('image', models.ImageField(blank=True, default='default.png', upload_to=users.utils.get_image_filename)),
                ('mobile_number', models.CharField(blank=True, max_length=12, null=True)),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('sex', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=6)),
                ('id_number', models.CharField(max_length=30, verbose_name='ID Number')),
                ('passport_number', models.CharField(blank=True, max_length=16, null=True)),
                ('residential_address', models.CharField(blank=True, max_length=30, null=True, verbose_name='Residential address')),
                ('district', models.CharField(blank=True, max_length=30, null=True)),
                ('gross_salary', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('tin_number', models.IntegerField(blank=True, null=True, verbose_name='TIN NUMBER')),
                ('appointment_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('social_security', models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3, null=True, verbose_name='Pays Social Security')),
                ('first_account_number', models.IntegerField(blank=True, null=True, verbose_name='Account Number 1')),
                ('second_account_number', models.IntegerField(blank=True, null=True, verbose_name='Account Number 2')),
                ('first_bank_percentage', models.IntegerField(blank=True, null=True, verbose_name='Percentage')),
                ('second_bank_percentage', models.IntegerField(blank=True, null=True, verbose_name='Percentage')),
                ('social_security_number', models.CharField(blank=True, max_length=30, null=True)),
                ('kin_full_name', models.CharField(blank=True, max_length=250, null=True)),
                ('kin_phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('kin_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('dr_ac_code', models.CharField(blank=True, max_length=30, null=True)),
                ('cr_ac_code', models.CharField(blank=True, max_length=30, null=True)),
                ('employment_status', models.CharField(blank=True, choices=[('RECRUIT', 'Recruit'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('TERMINATED', 'Terminated')], default='RECRUIT', max_length=17)),
                ('bank_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='first_bank', to='payroll.Bank')),
                ('bank_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='second_bank', to='payroll.Bank')),
                ('contract_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='support_data.ContractType')),
                ('cost_centre', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.CostCentre')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='payroll.Currency')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='support_data.Department')),
                ('duty_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='support_data.Country')),
                ('duty_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='support_data.DutyStation')),
                ('grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='support_data.Grade')),
                ('job_title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='support_data.JobTitle')),
                ('kin_relationship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='support_data.Relationship')),
                ('nationality', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='support_data.Nationality')),
                ('payroll_center', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='payroll.PayrollCenter')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=200)),
                ('cost_centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CostCentre')),
            ],
        ),
        migrations.CreateModel(
            name='TerminatedEmployees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('exit_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('days_given', models.IntegerField(null=True)),
                ('employable', models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3, null=True)),
                ('reason', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='SOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sof_code', models.CharField(max_length=20)),
                ('sof_name', models.CharField(max_length=200)),
                ('project_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Project')),
            ],
        ),
        migrations.CreateModel(
            name='PayrollProcessors',
            fields=[
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('payroll_key', models.CharField(blank=True, default=None, max_length=150, primary_key=True, serialize=False, unique=True)),
                ('earning_and_deductions_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payroll.EarningDeductionCategory')),
                ('earning_and_deductions_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payroll.EarningDeductionType')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Employee')),
                ('payroll_period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payroll.PayrollPeriod')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contribution_percentage', models.IntegerField(blank=True, null=True)),
                ('cost_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.CostCentre')),
                ('dea_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.DEA')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Employee')),
                ('project_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Project')),
                ('sof_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.SOF')),
            ],
        ),
        migrations.AddField(
            model_name='dea',
            name='sof_code',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.SOF'),
        ),
    ]
