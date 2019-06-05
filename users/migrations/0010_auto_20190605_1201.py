# Generated by Django 2.2 on 2019-06-05 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190605_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeproject',
            name='employee',
        ),
        migrations.AddField(
            model_name='employeeproject',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Employee'),
        ),
    ]
