# Generated by Django 2.0 on 2020-06-10 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendMatrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id1', models.IntegerField(blank=True, null=True)),
                ('id2', models.IntegerField(blank=True, null=True)),
                ('factor', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'matrix',
            },
        ),
    ]
