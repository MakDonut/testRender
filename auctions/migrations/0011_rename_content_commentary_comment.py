# Generated by Django 5.1 on 2024-10-03 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_commentary_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentary',
            old_name='content',
            new_name='comment',
        ),
    ]
