# Generated by Django 2.2 on 2019-04-03 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0003_auto_20190403_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payrollperiod',
            name='month',
            field=models.CharField(choices=[('JANUARY', 'JANUARY'), ('FEBRUARY', 'FEBRUARY'), ('MARCH', 'MARCH'), ('APRIL', 'APRIL'), ('MAY', 'MAY'), ('JUNE', 'JUNE'), ('JULY', 'JULY'), ('AUGUST', 'AUGUST'), ('SEPTEMBER', 'SEPTEMBER'), ('OCTOBER', 'OCTOBER'), ('NOVEMBER', 'NOVEMBER'), ('DECEMBER', 'DECEMBER')], default='APRIL', max_length=15),
        ),
    ]
