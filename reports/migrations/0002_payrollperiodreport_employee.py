# Generated by Django 2.2 on 2019-04-02 17:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reports', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollperiodreport',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Employee'),
        ),
    ]
