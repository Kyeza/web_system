# Generated by Django 2.2b1 on 2019-03-28 23:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employment_status',
            field=models.CharField(choices=[('RECRUIT', 'Recruit'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'),
                                            ('TERMINATED', 'Terminated')], default='RECRUIT', max_length=17),
        ),
    ]
