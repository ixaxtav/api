# Generated by Django 2.2.8 on 2020-12-01 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0103_auto_20201129_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='i9form',
            name='date_employee_signature',
            field=models.TextField(blank=True),
        ),
    ]
