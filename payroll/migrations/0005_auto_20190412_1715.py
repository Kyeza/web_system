# Generated by Django 2.2 on 2019-04-12 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0004_auto_20190412_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earningdeductiontype',
            name='export',
            field=models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', max_length=3, null=True),
        ),
    ]
