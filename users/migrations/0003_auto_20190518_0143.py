# Generated by Django 2.2 on 2019-05-17 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190518_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='cost_centre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.CostCentre'),
        ),
        migrations.AlterField(
            model_name='employeeproject',
            name='project_key',
            field=models.CharField(blank=True, editable=False, max_length=150),
        ),
        migrations.AlterField(
            model_name='payrollprocessors',
            name='payroll_key',
            field=models.CharField(blank=True, editable=False, max_length=150, primary_key=True, serialize=False, unique=True),
        ),
    ]
