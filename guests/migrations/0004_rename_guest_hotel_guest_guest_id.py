# Generated by Django 4.2.1 on 2023-06-21 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0003_rename_guest_id_hotel_guest_guest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel_guest',
            old_name='guest',
            new_name='guest_id',
        ),
    ]
