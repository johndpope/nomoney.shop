# Generated by Django 3.0.7 on 2020-07-11 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_location_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='chat',
        ),
    ]