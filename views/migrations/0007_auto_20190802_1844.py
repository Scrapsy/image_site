# Generated by Django 2.2.3 on 2019-08-02 16:44

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0006_auto_20190726_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='views/static/uploads/'), upload_to=''),
        ),
    ]
