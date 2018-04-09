# Generated by Django 2.0.3 on 2018-04-08 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('komiksy', '0024_auto_20180408_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='comic',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profil',
            name='comic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='komiksy.Comic'),
        ),
        migrations.AddField(
            model_name='profil',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]