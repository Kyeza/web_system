# Generated by Django 3.0.6 on 2020-09-24 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20200923_1214'),
        ('reports', '0015_auto_20200923_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankreport',
            name='summary_report',
        ),
        migrations.RemoveField(
            model_name='lstreport',
            name='summary_report',
        ),
        migrations.RemoveField(
            model_name='socialsecurityreport',
            name='summary_report',
        ),
        migrations.RemoveField(
            model_name='taxationreport',
            name='summary_report',
        ),
        migrations.AddField(
            model_name='bankreport',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Employee'),
        ),
        migrations.AddField(
            model_name='lstreport',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Employee'),
        ),
        migrations.AddField(
            model_name='socialsecurityreport',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Employee'),
        ),
        migrations.AddField(
            model_name='taxationreport',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Employee'),
        ),
        migrations.AlterField(
            model_name='extrasummaryreportinfo',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Employee'),
        ),
    ]