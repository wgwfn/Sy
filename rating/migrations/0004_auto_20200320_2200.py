# Generated by Django 2.2.2 on 2020-03-20 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0003_auto_20200320_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='movies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movie.Movie'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]
