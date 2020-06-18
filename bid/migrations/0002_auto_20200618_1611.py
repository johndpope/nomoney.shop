# Generated by Django 3.0.7 on 2020-06-18 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listing', '0001_initial'),
        ('bid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidpush',
            name='push',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Push'),
        ),
        migrations.AddField(
            model_name='bidpush',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Unit'),
        ),
        migrations.AddField(
            model_name='bidpull',
            name='bid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bid.Bid'),
        ),
        migrations.AddField(
            model_name='bidpull',
            name='pull',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Pull'),
        ),
        migrations.AddField(
            model_name='bidpull',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Unit'),
        ),
    ]
