# Generated by Django 2.2.4 on 2020-01-06 02:51

from django.db import migrations

from api.models import PreDefinedDeduction


def load(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    PreDefinedDeductionModel = apps.get_model('api', 'PreDefinedDeduction')
    deductions = [{
        "name": "Social Security",
        "type": PreDefinedDeduction.PERCENTAGE_TYPE,
        "value": 5.0,
    }, {
        "name": "Medicare",
        "type": PreDefinedDeduction.PERCENTAGE_TYPE,
        "value": 5.0,
    }
    ]
    [PreDefinedDeductionModel.objects.create(**i) for i in deductions]


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0067_employerdeduction_predefineddeduction'),
    ]

    operations = [
        migrations.RunPython(load),

    ]
