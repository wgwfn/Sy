# Generated by Django 2.0 on 2020-04-17 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_auto_20200417_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='douban',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imbd',
            field=models.TextField(blank=True, null=True),
        ),
    ]
