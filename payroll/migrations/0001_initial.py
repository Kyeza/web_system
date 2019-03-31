# Generated by Django 2.2b1 on 2019-03-31 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('support_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=150)),
                ('sort_code', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=150)),
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
                ('ed_type', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=150)),
                ('recurrent', models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3)),
                ('taxable', models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3)),
                ('ed_category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING,
                                                  to='payroll.EarningDeductionCategory')),
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
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support_data.Country')),
                ('organization',
                 models.ForeignKey(null=True, on_delete=models.SET(None), to='support_data.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='PayrollPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], default=3)),
                ('year', models.IntegerField(choices=[(2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028)], default=2019)),
                ('payroll_key', models.CharField(blank=True, default=None, max_length=150)),
                ('status',
                 models.CharField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed')], default='CLOSED', max_length=6)),
                ('payroll_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.PayrollCenter')),
            ],
        ),
        migrations.CreateModel(
            name='PayrollCenterEds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ed_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                              to='payroll.EarningDeductionType')),
                ('payroll_center',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.PayrollCenter')),
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
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                              to='support_data.Country')),
            ],
        ),
    ]
