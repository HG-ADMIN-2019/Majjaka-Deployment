# Generated by Django 3.1.7 on 2022-10-27 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Configuration', '0010_auto_20221026_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='producteformpricing',
            name='variant_config_guid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.variantconfig'),
        ),
    ]
