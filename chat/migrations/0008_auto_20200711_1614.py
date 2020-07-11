# Generated by Django 3.0.7 on 2020-07-11 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20200711_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='location',
        ),
        migrations.AlterField(
            model_name='chat',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'default'), (10, 'user'), (20, 'market'), (100, 'lobby')], default=0),
        ),
    ]