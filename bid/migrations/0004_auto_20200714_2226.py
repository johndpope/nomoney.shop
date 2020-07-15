# Generated by Django 3.0.7 on 2020-07-14 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deal', '0005_auto_20200714_2226'),
        ('listing', '0005_auto_20200714_2226'),
        ('bid', '0003_auto_20200714_1425'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'get_latest_by': ['datetime'], 'ordering': ['-datetime'], 'verbose_name': 'bid', 'verbose_name_plural': 'bids'},
        ),
        migrations.AlterModelOptions(
            name='bidposition',
            options={'verbose_name': 'bidposition', 'verbose_name_plural': 'bidpositions'},
        ),
        migrations.AlterField(
            model_name='bid',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='deal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deal.Deal', verbose_name='deal'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'unseen'), (10, 'seen'), (30, 'answered'), (100, 'accepted'), (110, 'rejected')], default=0, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='bidposition',
            name='bid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bid.Bid', verbose_name='bid'),
        ),
        migrations.AlterField(
            model_name='bidposition',
            name='push',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Push', verbose_name='push'),
        ),
        migrations.AlterField(
            model_name='bidposition',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name='quantity'),
        ),
        migrations.AlterField(
            model_name='bidposition',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Unit', verbose_name='unit'),
        ),
    ]