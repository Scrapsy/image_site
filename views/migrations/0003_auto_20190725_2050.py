# Generated by Django 2.2.3 on 2019-07-25 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0002_auto_20190725_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(upload_to='views/static/uploads/'),
        ),
    ]
