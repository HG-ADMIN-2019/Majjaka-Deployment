# Generated by Django 3.1.7 on 2022-09-12 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Generate_OTP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpgenerator',
            name='password',
            field=models.CharField(db_column='PASSWORD', max_length=256, null=True),
        ),
    ]
