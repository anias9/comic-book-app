# Generated by Django 2.0.3 on 2018-04-08 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('komiksy', '0027_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='comic',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='user',
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
