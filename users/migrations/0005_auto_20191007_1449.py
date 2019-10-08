# Generated by Django 2.2 on 2019-10-07 14:49

from django.db import migrations, models
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20191004_0947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='cr_ac_code',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='dr_ac_code',
        ),
        migrations.AddField(
            model_name='employee',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to=users.utils.get_doc_filename),
        ),
    ]
