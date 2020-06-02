# Generated by Django 3.0.6 on 2020-06-02 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0006_payrollperiod_created_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bank',
            options={'ordering': ['bank'], 'verbose_name': 'Bank', 'verbose_name_plural': 'Banks'},
        ),
        migrations.AddField(
            model_name='bank',
            name='branch_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payrollperiod',
            name='month',
            field=models.CharField(choices=[('JANUARY', 'JANUARY'), ('FEBRUARY', 'FEBRUARY'), ('MARCH', 'MARCH'), ('APRIL', 'APRIL'), ('MAY', 'MAY'), ('JUNE', 'JUNE'), ('JULY', 'JULY'), ('AUGUST', 'AUGUST'), ('SEPTEMBER', 'SEPTEMBER'), ('OCTOBER', 'OCTOBER'), ('NOVEMBER', 'NOVEMBER'), ('DECEMBER', 'DECEMBER')], db_index=True, default='JUNE', max_length=15),
        ),
    ]
