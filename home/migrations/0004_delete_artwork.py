# Generated by Django 5.1.1 on 2024-10-29 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_alter_feedback_artwork'),
        ('home', '0003_artwork_tags_alter_artwork_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Artwork',
        ),
    ]