# Generated by Django 4.2 on 2024-05-06 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_merge_20240506_2351'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reservation_Itineraire',
        ),
    ]