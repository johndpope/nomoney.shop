# Generated by Django 3.0.5 on 2020-04-05 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0005_auto_20200405_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
