# Generated by Django 3.2 on 2021-04-22 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_auto_20210422_0556'),
    ]

    operations = [
        migrations.AddField(
            model_name='mod',
            name='model_favs',
            field=models.IntegerField(default=0),
        ),
    ]