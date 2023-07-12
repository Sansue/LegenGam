# Generated by Django 4.2.2 on 2023-06-20 07:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("graph", "0005_champstats"),
    ]

    operations = [
        migrations.AddField(
            model_name="champstats",
            name="champ_kda",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="champstats",
            name="champ_lvl",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="champstats",
            name="champ_winrate",
            field=models.FloatField(default=0),
        ),
    ]
