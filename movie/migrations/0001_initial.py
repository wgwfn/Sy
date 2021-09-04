# Generated by Django 2.2.2 on 2020-03-20 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('genres', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'movie',
            },
        ),
    ]