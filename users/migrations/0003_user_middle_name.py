# Generated by Django 3.0.6 on 2020-06-04 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_employee_current_payroll_category_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
