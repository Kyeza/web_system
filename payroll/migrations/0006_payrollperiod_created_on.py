# Generated by Django 3.0.6 on 2020-05-23 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_auto_20200523_0134'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollperiod',
            name='created_on',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
    ]
