# Generated by Django 2.2 on 2019-10-22 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_data', '0002_auto_20191011_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='movementparameter',
            name='choice',
            field=models.IntegerField(null=True),
        ),
    ]
