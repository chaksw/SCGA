# Generated by Django 5.0.6 on 2024-06-23 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scgaapi', '0011_alter_scga_file_name_alter_testexception_scga_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defectclassification',
            name='non_tech',
            field=models.CharField(choices=[('Y', 'Y'), ('N', 'N'), ('NA', 'NA')], default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='defectclassification',
            name='process',
            field=models.CharField(choices=[('Y', 'Y'), ('N', 'N'), ('NA', 'NA')], default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='defectclassification',
            name='tech',
            field=models.CharField(choices=[('Y', 'Y'), ('N', 'N'), ('NA', 'NA')], default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='scgafunction',
            name='oversight',
            field=models.CharField(choices=[('Y', 'Y'), ('N', 'N'), ('NA', 'NA')], default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='testexception',
            name='level',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('NA', 'NA')], default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='testplan',
            name='level',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('NA', 'NA')], default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='uncoverage',
            name='_class',
            field=models.CharField(choices=[('incomplete Tests', 'Incomplete Tests'), ('requirements-code mismatch', 'Requirements-Code Mismatch'), ('deactivated code', 'Deactivated Code'), ('defensive code', 'Defensive Code'), ('test environment limitations', 'Test Environment Limitations'), ('previously analyzed software', 'Previously Analyzed Software'), ('other', 'Other'), ('NA', 'NA')], default='NA', max_length=255),
        ),
        migrations.AlterField(
            model_name='uncoverage',
            name='issue',
            field=models.CharField(choices=[('Y', 'Y'), ('N', 'N'), ('NA', 'NA')], default='NA', max_length=20),
        ),
    ]