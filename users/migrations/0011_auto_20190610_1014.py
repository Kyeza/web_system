# Generated by Django 2.2 on 2019-06-10 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20190605_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeproject',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Employee'),
        ),
    ]
