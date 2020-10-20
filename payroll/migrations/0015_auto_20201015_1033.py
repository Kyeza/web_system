# Generated by Django 3.0.6 on 2020-10-15 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0014_auto_20200923_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payrollperiod',
            name='month',
            field=models.CharField(choices=[('JANUARY', 'JANUARY'), ('FEBRUARY', 'FEBRUARY'), ('MARCH', 'MARCH'), ('APRIL', 'APRIL'), ('MAY', 'MAY'), ('JUNE', 'JUNE'), ('JULY', 'JULY'), ('AUGUST', 'AUGUST'), ('SEPTEMBER', 'SEPTEMBER'), ('OCTOBER', 'OCTOBER'), ('NOVEMBER', 'NOVEMBER'), ('DECEMBER', 'DECEMBER')], db_index=True, default='OCTOBER', max_length=15),
        ),
    ]