# Generated by Django 4.2 on 2024-06-21 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scgaapi', '0002_coverage_defectclassification_modulestrucdata_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='covered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branches', models.IntegerField()),
                ('pairs', models.IntegerField()),
                ('statement', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='total',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branches', models.IntegerField()),
                ('pairs', models.IntegerField()),
                ('statement', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='moduleStrucData',
        ),
        migrations.AddField(
            model_name='coverage',
            name='function',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scgaapi.scgafunction'),
        ),
        migrations.AddField(
            model_name='defectclassification',
            name='unction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scgaapi.scgafunction'),
        ),
        migrations.AddField(
            model_name='scgafunction',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='functions', to='scgaapi.scgamodule'),
        ),
        migrations.AddField(
            model_name='scgamodule',
            name='test_exception',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='scgaapi.testexception'),
        ),
        migrations.AddField(
            model_name='scgamodule',
            name='test_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='scgaapi.testplan'),
        ),
        migrations.AddField(
            model_name='uncoverage',
            name='function',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uncoverage', to='scgaapi.scgafunction'),
        ),
        migrations.AddField(
            model_name='total',
            name='function',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scgaapi.scgafunction'),
        ),
        migrations.AddField(
            model_name='covered',
            name='function',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scgaapi.scgafunction'),
        ),
    ]