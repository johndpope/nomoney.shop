# Generated by Django 3.0.7 on 2020-07-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_remove_market_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='test',
            field=models.BooleanField(default=False),
        ),
    ]
