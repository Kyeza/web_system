# Generated by Django 3.0.6 on 2020-08-20 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0014_auto_20200605_0638'),
        ('users', '0011_auto_20200729_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayIdCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_id', models.PositiveIntegerField(default=1)),
                ('end_id', models.PositiveIntegerField(default=1000)),
                ('current_id', models.PositiveIntegerField(default=0)),
                ('previous_id', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Display ID',
            },
        ),
        migrations.AlterField(
            model_name='payrollprocessors',
            name='summary_report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='earning_or_deduction', to='reports.ExtraSummaryReportInfo'),
        ),
    ]
