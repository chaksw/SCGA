# Generated by Django 5.0.6 on 2024-07-03 01:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scgaapi', '0020_alter_uncoverage_uncovered_sw_line'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scgamodule',
            name='test_exception',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='temodules', to='scgaapi.testexception'),
        ),
        migrations.AlterField(
            model_name='scgamodule',
            name='test_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tpmodules', to='scgaapi.testplan'),
        ),
    ]
