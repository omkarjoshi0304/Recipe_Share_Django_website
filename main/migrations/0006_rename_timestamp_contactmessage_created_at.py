# Generated by Django 5.2 on 2025-04-16 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_submitted_at_contactmessage_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmessage',
            old_name='timestamp',
            new_name='created_at',
        ),
    ]
