# Generated by Django 3.0.5 on 2020-04-04 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0004_auto_20200404_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='title',
            field=models.CharField(default='saf', max_length=100),
            preserve_default=False,
        ),
    ]
