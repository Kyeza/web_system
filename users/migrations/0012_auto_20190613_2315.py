# Generated by Django 2.2 on 2019-06-13 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20190610_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='user_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group'),
        ),
    ]