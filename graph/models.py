from django.db import models
from django.urls import reverse


class Data(models.Model):
    championid = models.IntegerField()
    ss1 = models.IntegerField()
    ss2 = models.IntegerField()
    role = models.CharField(blank=True, null=True)
    position = models.CharField(blank=True, null=True)
    win = models.IntegerField()
    item1 = models.IntegerField()
    item2 = models.IntegerField()
    item3 = models.IntegerField()
    item4 = models.IntegerField()
    item5 = models.IntegerField()
    item6 = models.IntegerField()
    trinket = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    largestkillingspree = models.IntegerField()
    largestmultikill = models.IntegerField()
    killingsprees = models.IntegerField()
    longesttimespentliving = models.IntegerField()
    doublekills = models.IntegerField()
    triplekills = models.IntegerField()
    quadrakills = models.IntegerField()
    pentakills = models.IntegerField()
    legendarykills = models.IntegerField()
    totdmgdealt = models.IntegerField()
    magicdmgdealt = models.IntegerField()
    physicaldmgdealt = models.IntegerField()
    truedmgdealt = models.IntegerField()
    largestcrit = models.IntegerField()
    totdmgtochamp = models.IntegerField()
    magicdmgtochamp = models.IntegerField()
    physdmgtochamp = models.IntegerField()
    truedmgtochamp = models.IntegerField()
    totheal = models.IntegerField()
    totunitshealed = models.IntegerField()
    dmgselfmit = models.IntegerField()
    dmgtoobj = models.IntegerField()
    dmgtoturrets = models.IntegerField()
    visionscore = models.IntegerField()
    timecc = models.IntegerField()
    totdmgtaken = models.IntegerField()
    magicdmgtaken = models.IntegerField()
    physdmgtaken = models.IntegerField()
    truedmgtaken = models.IntegerField()
    goldearned = models.IntegerField()
    goldspent = models.IntegerField()
    turretkills = models.IntegerField()
    inhibkills_x = models.IntegerField()
    totminionskilled = models.IntegerField()
    neutralminionskilled = models.IntegerField()
    ownjunglekills = models.IntegerField()
    enemyjunglekills = models.IntegerField()
    totcctimedealt = models.IntegerField()
    champlvl = models.IntegerField()
    pinksbought = models.IntegerField()
    wardsbought = models.IntegerField()
    wardsplaced = models.IntegerField()
    wardskilled = models.IntegerField()
    firstblood = models.IntegerField()
    firsttower = models.IntegerField()
    firstinhib = models.IntegerField()
    firstbaron = models.IntegerField()
    firstdragon = models.IntegerField()
    firstharry = models.IntegerField()
    towerkills = models.IntegerField()
    inhibkills_y = models.IntegerField()
    baronkills = models.IntegerField()
    dragonkills = models.IntegerField()
    harrykills = models.IntegerField()

    class Meta:
        managed = False
        verbose_name = "Data"


class Champs(models.Model):
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "champs"


class ChampStats(models.Model):
    champ_top_count = models.IntegerField(default=0)
    champ_jungle_count = models.IntegerField(default=0)
    champ_mid_count = models.IntegerField(default=0)
    champ_adc_count = models.IntegerField(default=0)
    champ_support_count = models.IntegerField(default=0)
    champ_count = models.IntegerField(default=0)
    champ_winrate = models.FloatField(default=0)
    champ_kda = models.FloatField(default=0)
    champ_lvl = models.FloatField(default=0)
    champ_dmgtype = models.CharField(max_length=50, default="", null=True, blank=True)
    champ_item_set_one_item = models.JSONField(default=dict, null=True, blank=True)
    champ_item_set_two_item = models.JSONField(default=dict, null=True, blank=True)
    champ_item_set_three_item = models.JSONField(default=dict, null=True, blank=True)
    champ_item_set_four_item = models.JSONField(default=dict, null=True, blank=True)
    champ_item_set_five_item = models.JSONField(default=dict, null=True, blank=True)
    champ_item_set_six_item = models.JSONField(default=dict, null=True, blank=True)
    champ = models.OneToOneField(Champs, on_delete=models.CASCADE)

    def __str__(self):
        return self.champ.name


class Items(models.Model):
    name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "items"


class SummonerSpells(models.Model):
    name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "summoner_spells"
