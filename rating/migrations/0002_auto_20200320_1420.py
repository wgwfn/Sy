# Generated by Django 2.2.2 on 2020-03-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='movies_id',
            new_name='movies',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='rating',
            name='timeStamp',
            field=models.DateField(blank=True, null=True),
        ),
    ]
