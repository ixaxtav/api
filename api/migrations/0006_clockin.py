# Generated by Django 2.0 on 2018-10-23 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20181019_2020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clockin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(blank=True)),
                ('ended_at', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Profile')),
                ('employee', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.Employee')),
                ('shift', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.Shift')),
            ],
        ),
    ]
