# Generated by Django 2.2 on 2019-05-29 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0004_auto_20190528_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earningdeductiontype',
            name='factor',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
