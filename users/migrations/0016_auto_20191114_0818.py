# Generated by Django 2.2.7 on 2019-11-14 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20191113_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeemovement',
            name='hours',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
