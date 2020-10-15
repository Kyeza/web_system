# Generated by Django 3.0.6 on 2020-10-15 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20200924_1146'),
        ('reports', '0018_merge_20201014_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankreport',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Employee'),
        ),
        migrations.AddField(
            model_name='lstreport',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Employee'),
        ),
        migrations.AddField(
            model_name='socialsecurityreport',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Employee'),
        ),
        migrations.AddField(
            model_name='taxationreport',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Employee'),
        ),
    ]
