# Generated by Django 3.0.6 on 2020-05-23 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='current_payroll_category_id',
            field=models.PositiveIntegerField(editable=False, null=True),
        ),
    ]