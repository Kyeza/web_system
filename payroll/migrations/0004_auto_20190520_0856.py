# Generated by Django 2.2 on 2019-05-20 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0003_auto_20190518_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earningdeductiontype',
            name='ed_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]