# Generated by Django 3.1.7 on 2022-08-08 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Shopping_Cart', '0004_auto_20220802_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheader',
            name='follow_on_doc_type',
            field=models.CharField(db_column='FOLLOW_ON_DOC_TYPE', max_length=5, null=True),
        ),
    ]