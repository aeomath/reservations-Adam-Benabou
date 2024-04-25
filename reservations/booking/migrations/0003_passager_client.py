# Generated by Django 4.2 on 2024-04-25 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0002_alter_reservation_numero_reservation"),
    ]

    operations = [
        migrations.AddField(
            model_name="passager",
            name="Client",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="booking.client",
            ),
        ),
    ]