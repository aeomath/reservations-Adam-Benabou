# Generated by Django 4.2 on 2024-04-16 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0007_alter_client_nom_alter_client_prénom"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reservation", models.DateTimeField()),
                ("numero_reservation", models.IntegerField()),
                ("numero_voiture", models.IntegerField()),
                ("numero_place", models.IntegerField()),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="booking.client"
                    ),
                ),
                (
                    "passager",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="booking.passager",
                    ),
                ),
                (
                    "trajet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="booking.trajet"
                    ),
                ),
            ],
        ),
    ]
