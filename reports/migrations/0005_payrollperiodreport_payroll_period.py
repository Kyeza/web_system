# Generated by Django 2.2 on 2019-04-03 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0004_auto_20190403_1052'),
        ('reports', '0004_auto_20190403_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollperiodreport',
            name='payroll_period',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payroll.PayrollPeriod'),
        ),
    ]
