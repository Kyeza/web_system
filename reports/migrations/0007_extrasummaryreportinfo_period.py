# Generated by Django 3.0.6 on 2020-06-04 08:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_auto_20200604_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='extrasummaryreportinfo',
            name='period',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
