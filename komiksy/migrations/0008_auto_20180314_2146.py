# Generated by Django 2.0.3 on 2018-03-14 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komiksy', '0007_auto_20180312_1533'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comic',
            options={'ordering': ['-created'], 'verbose_name': 'komiks', 'verbose_name_plural': 'komiksy'},
        ),
        migrations.AddField(
            model_name='comic',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]