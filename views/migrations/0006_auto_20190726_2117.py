# Generated by Django 2.2.3 on 2019-07-26 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0005_keyword_uses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='uses',
            field=models.IntegerField(default=0),
        ),
    ]
