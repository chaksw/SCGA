# Generated by Django 5.0.6 on 2024-06-25 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scgaapi', '0014_remove_testexception_scga_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testexception',
            name='level',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_exceptions', to='scgaapi.level'),
        ),
    ]
