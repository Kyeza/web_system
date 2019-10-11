# Generated by Django 2.2 on 2019-10-10 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payroll', '0002_auto_20191010_1242'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollapprover',
            name='approver',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organization',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support_data.Country'),
        ),
        migrations.AddField(
            model_name='dutystation',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support_data.Country'),
        ),
        migrations.AddField(
            model_name='dutystation',
            name='earnings_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payroll.EarningDeductionType'),
        ),
    ]
