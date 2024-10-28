# Generated by Django 5.1.1 on 2024-10-26 15:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_participants'),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='gallery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gallery.gallery'),
        ),
    ]