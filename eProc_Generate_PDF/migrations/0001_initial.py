# Generated by Django 3.1.7 on 2022-08-23 17:14

from django.db import migrations, models
import django.db.models.deletion
import eProc_Generate_PDF.models.document_pdf


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eProc_Configuration', '0006_posplittype_del_ind'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentPdf',
            fields=[
                ('document_pdf_guid', models.CharField(db_column='DOCUMENT_PDF_GUID', max_length=32, primary_key=True, serialize=False)),
                ('doc_num', models.CharField(db_column='DOC_NUMBER', max_length=10, verbose_name='DOC Number')),
                ('doc_file', models.FileField(db_column='DOC_FILE', upload_to=eProc_Generate_PDF.models.document_pdf.DocumentPdf.get_file_path)),
                ('document_pdf_created_at', models.DateTimeField(db_column='DOCUMENT_PDF_CREATED_AT', null=True)),
                ('document_pdf_created_by', models.CharField(db_column='DOCUMENT_PDF_CREATED_BY', max_length=12, null=True)),
                ('document_pdf_changed_at', models.DateTimeField(blank=True, db_column='DOCUMENT_PDF_CHANGED_AT', null=True)),
                ('document_pdf_changed_by', models.CharField(db_column='DOCUMENT_PDF_CHANGED_BY', max_length=12, null=True)),
                ('document_pdf_source_system', models.CharField(db_column='DOCUMENT_PDF_SOURCE_SYSTEM', max_length=20)),
                ('document_pdf_destination_system', models.CharField(db_column='DOCUMENT_PDF_DESTINATION_SYSTEM', max_length=20)),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
                ('document_type', models.ForeignKey(db_column='DOCUMENT_TYPE', default=None, on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.documenttype')),
            ],
            options={
                'db_table': 'MTD_DOCUMENT_PDF',
                'managed': True,
            },
        ),
    ]