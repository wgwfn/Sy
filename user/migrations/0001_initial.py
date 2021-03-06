# Generated by Django 2.2.2 on 2020-03-20 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('work', models.IntegerField(blank=True, null=True)),
                ('username', models.CharField(blank=True, max_length=16, null=True)),
                ('nickname', models.CharField(blank=True, max_length=16, null=True)),
                ('password', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
