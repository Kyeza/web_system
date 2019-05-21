# Generated by Django 2.2 on 2019-05-18 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracttype',
            name='contract_expiry',
            field=models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='contracttype',
            name='contract_type',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='contracttype',
            name='leave_days_entitled',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='contracttype',
            name='leave_entitled',
            field=models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3, null=True),
        ),
    ]