# Generated by Django 2.0 on 2018-11-29 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20181129_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='clockin',
            name='latitude',
            field=models.DecimalField(decimal_places=11, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='clockin',
            name='longitude',
            field=models.DecimalField(decimal_places=11, default=0, max_digits=14),
        ),
    ]
