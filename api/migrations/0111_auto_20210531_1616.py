# Generated by Django 2.2.8 on 2021-05-31 16:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0110_auto_20201228_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='w4form',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='w4form',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
