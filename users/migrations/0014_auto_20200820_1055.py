# Generated by Django 3.0.6 on 2020-08-20 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0014_auto_20200605_0638'),
        ('users', '0013_auto_20200820_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payrollprocessors',
            name='summary_report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='earning_or_deduction', to='reports.ExtraSummaryReportInfo'),
        ),
    ]
