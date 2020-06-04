# Generated by Django 3.0.6 on 2020-05-20 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=150)),
                ('branch', models.CharField(blank=True, max_length=200, null=True)),
                ('sort_code', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_code', models.CharField(blank=True, max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='EarningDeductionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EarningDeductionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ed_type', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('account_name', models.CharField(blank=True, max_length=200, null=True)),
                ('recurrent', models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3)),
                ('taxable', models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3)),
                ('export', models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', max_length=3, null=True)),
                ('factor', models.FloatField(blank=True, default=0, null=True)),
                ('summarize', models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', max_length=3, null=True)),
                ('agresso_type', models.CharField(blank=True, choices=[('STAFF ADVANCES', 'STAFF ADVANCES'), ('ACCRUED PAYROLL', 'ACCRUED PAYROLL'), ('EMPLOYEE PENSION', 'EMPLOYEE PENSION'), ('STAFF EXPENSES', 'STAFF EXPENSES'), ('SALARY ADVANCES', 'SALARY ADVANCES'), ('PAYE', 'PAYE'), ('SOCIAL SECURITY', 'SOCIAL SECURITY'), ('SALARIES', 'SALARIES'), ('OVERTIME', 'OVERTIME'), ('ADDITIONAL SALARY COSTS', 'ADDITIONAL SALARY COSTS'), ('BENEFIT - LIVING ACCOMMODATION', 'BENEFIT - LIVING ACCOMMODATION'), ('SEVERANCE PAYMENTS', 'SEVERANCE PAYMENTS'), ('PENSION COSTS', 'PENSION COSTS')], max_length=50, null=True)),
                ('account_code', models.CharField(blank=True, max_length=15, null=True)),
                ('debit_credit_sign', models.CharField(blank=True, max_length=15, null=True)),
                ('display_number', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LSTRates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_boundary', models.DecimalField(decimal_places=2, max_digits=12)),
                ('upper_boundary', models.DecimalField(decimal_places=2, max_digits=12)),
                ('fixed_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='PAYERates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_boundary', models.DecimalField(decimal_places=2, max_digits=12)),
                ('upper_boundary', models.DecimalField(decimal_places=2, max_digits=12)),
                ('fixed_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='PayrollCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('date_create', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayrollCenterEds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pced_key', models.CharField(blank=True, default=None, max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayrollPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('JANUARY', 'JANUARY'), ('FEBRUARY', 'FEBRUARY'), ('MARCH', 'MARCH'), ('APRIL', 'APRIL'), ('MAY', 'MAY'), ('JUNE', 'JUNE'), ('JULY', 'JULY'), ('AUGUST', 'AUGUST'), ('SEPTEMBER', 'SEPTEMBER'), ('OCTOBER', 'OCTOBER'), ('NOVEMBER', 'NOVEMBER'), ('DECEMBER', 'DECEMBER')], db_index=True, default='MAY', max_length=15)),
                ('year', models.IntegerField(choices=[(2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029)], db_index=True, default=2020)),
                ('payroll_key', models.CharField(blank=True, default=None, max_length=150, unique=True)),
                ('status', models.CharField(default='OPEN', max_length=6)),
            ],
            options={
                'permissions': [('close_payrollperiod', 'Can close payroll period'), ('process_payrollperiod', 'Can process payroll period')],
            },
        ),
    ]
