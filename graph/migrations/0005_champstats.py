# Generated by Django 4.2.2 on 2023-06-19 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("graph", "0004_summonerspells"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChampStats",
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
                ("champ_top_count", models.IntegerField(default=0)),
                ("champ_jungle_count", models.IntegerField(default=0)),
                ("champ_mid_count", models.IntegerField(default=0)),
                ("champ_adc_count", models.IntegerField(default=0)),
                ("champ_support_count", models.IntegerField(default=0)),
                ("champ_count", models.IntegerField(default=0)),
                (
                    "champ",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="graph.champs"
                    ),
                ),
            ],
        ),
    ]
