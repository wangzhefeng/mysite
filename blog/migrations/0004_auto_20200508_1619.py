# Generated by Django 2.1.5 on 2020-05-08 16:19

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200508_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
