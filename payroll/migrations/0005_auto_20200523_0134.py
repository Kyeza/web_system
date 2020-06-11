# Generated by Django 3.0.6 on 2020-05-23 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('payroll', '0004_auto_20200523_0107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payrollperiod',
            name='staff_category',
        ),
        migrations.AddField(
            model_name='payrollcenter',
            name='staff_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Category'),
        ),
    ]
