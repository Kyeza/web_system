# Generated by Django 3.0.6 on 2020-06-25 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0007_auto_20200602_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='bank_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
