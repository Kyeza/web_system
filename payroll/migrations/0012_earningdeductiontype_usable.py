# Generated by Django 3.0.6 on 2020-08-20 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0011_auto_20200820_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='earningdeductiontype',
            name='usable',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', max_length=3, null=True, verbose_name='Should this enumaration be added to current Payroll Period'),
        ),
    ]