# Generated by Django 2.2 on 2019-05-29 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190526_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='agresso_number',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='id_number',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
    ]