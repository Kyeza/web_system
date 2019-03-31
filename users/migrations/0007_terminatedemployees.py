# Generated by Django 2.2b1 on 2019-03-30 10:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0006_auto_20190329_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='TerminatedEmployees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('exit_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('termination_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('days_given', models.IntegerField(max_length=150, null=True)),
                ('employable',
                 models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3, null=True)),
                ('reason', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Employee')),
            ],
        ),
    ]
