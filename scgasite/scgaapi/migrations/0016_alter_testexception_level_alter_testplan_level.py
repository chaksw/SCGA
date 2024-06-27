# Generated by Django 5.0.6 on 2024-06-27 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scgaapi', '0015_alter_testexception_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testexception',
            name='level',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_exception', to='scgaapi.level'),
        ),
        migrations.AlterField(
            model_name='testplan',
            name='level',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_plan', to='scgaapi.level'),
        ),
    ]