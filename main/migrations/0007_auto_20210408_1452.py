# Generated by Django 2.2.19 on 2021-04-08 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_mod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mod',
            name='model_downloads',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mod',
            name='model_views',
            field=models.IntegerField(default=0),
        ),
    ]