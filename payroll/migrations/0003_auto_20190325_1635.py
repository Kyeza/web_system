# Generated by Django 2.2b1 on 2019-03-25 13:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payroll', '0002_auto_20190325_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payrollcenter',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
