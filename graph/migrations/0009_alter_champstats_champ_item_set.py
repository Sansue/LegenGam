# Generated by Django 4.2.2 on 2023-06-23 12:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("graph", "0008_champstats_champ_item_set"),
    ]

    operations = [
        migrations.AlterField(
            model_name="champstats",
            name="champ_item_set",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]