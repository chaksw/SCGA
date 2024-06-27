# Generated by Django 5.0.6 on 2024-06-27 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scgaapi', '0016_alter_testexception_level_alter_testplan_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uncoverage',
            name='function',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uncoverages', to='scgaapi.scgafunction'),
        ),
    ]
