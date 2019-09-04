# Generated by Django 2.2 on 2019-09-04 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExTraSummaryReportInfo',
            fields=[
                ('key', models.CharField(blank=True, default=None, max_length=150, primary_key=True, serialize=False, unique=True)),
                ('analysis', models.CharField(blank=True, max_length=150, null=True)),
                ('employee_name', models.CharField(blank=True, max_length=250, null=True)),
                ('job_title', models.CharField(blank=True, max_length=150, null=True)),
                ('total_deductions', models.DecimalField(decimal_places=2, default=None, max_digits=12)),
                ('net_pay', models.DecimalField(decimal_places=2, default=None, max_digits=12)),
                ('gross_earning', models.DecimalField(decimal_places=2, default=None, max_digits=12)),
            ],
        ),
    ]
