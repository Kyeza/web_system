# Generated by Django 2.2 on 2019-05-17 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190518_0151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='terminatedemployees',
            name='id',
        ),
        migrations.AlterField(
            model_name='terminatedemployees',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.Employee'),
        ),
    ]