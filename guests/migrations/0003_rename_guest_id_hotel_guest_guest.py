# Generated by Django 4.2.1 on 2023-06-21 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0002_alter_hotel_guest_guest_comm_dweller'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel_guest',
            old_name='guest_id',
            new_name='guest',
        ),
    ]
