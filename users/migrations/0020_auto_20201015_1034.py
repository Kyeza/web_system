# Generated by Django 3.0.6 on 2020-10-15 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0019_auto_20201015_1033'),
        ('users', '0019_auto_20201015_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payrollprocessors',
            name='summary_report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='earning_or_deduction', to='reports.ExtraSummaryReportInfo'),
        ),
    ]
