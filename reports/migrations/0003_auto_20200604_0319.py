# Generated by Django 3.0.6 on 2020-06-04 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20200520_1742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extrasummaryreportinfo',
            old_name='key',
            new_name='report_id',
        ),
    ]