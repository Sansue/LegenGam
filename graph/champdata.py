import json
from django.db.models import Avg, When, Case, Value, Q, Count, F
from django.templatetags.static import static
from graph.models import Data, Champs, Items, SummonerSpells, ChampStats
from graph import champdata_ajax
import os
import random

absolute_path = os.path.dirname(__file__)


def statsbyposition(position=None):
    top = Data.objects.filter(position="TOP").aggregate(
        top_winrate=((Avg("win") * 100) - 49) / 2,
        top_kda=(Avg("kills") + Avg("assists")) / Avg("deaths") - 2,
        top_gold=(Avg("goldearned") / 1000 - 9.5) / 3,
        top_timeliving=(Avg("longesttimespentliving") - 600) / 100,
        top_cs=Avg("totminionskilled") / 200,
        top_vision=Avg("visionscore") / 30,
        top_lvl=(Avg("champlvl") - 10) / 8,
    )
    jungle = Data.objects.filter(position="JUNGLE").aggregate(
        jungle_winrate=((Avg("win") * 100) - 49) / 2,
        jungle_kda=(Avg("kills") + Avg("assists")) / Avg("deaths") - 2,
        jungle_gold=(Avg("goldearned") / 1000 - 9.5) / 3,
        jungle_timeliving=(Avg("longesttimespentliving") - 600) / 100,
        jungle_cs=Avg("totminionskilled") / 200,
        jungle_vision=Avg("visionscore") / 30,
        jungle_lvl=(Avg("champlvl") - 10) / 8,
    )
    mid = Data.objects.filter(position="MID").aggregate(
        mid_winrate=((Avg("win") * 100) - 49) / 2,
        mid_kda=(Avg("kills") + Avg("assists")) / Avg("deaths") - 2,
        mid_gold=(Avg("goldearned") / 1000 - 9.5) / 3,
        mid_timeliving=(Avg("longesttimespentliving") - 600) / 100,
        mid_cs=Avg("totminionskilled") / 200,
        mid_vision=Avg("visionscore") / 30,
        mid_lvl=(Avg("champlvl") - 10) / 8,
    )
    adc = Data.objects.filter(position="ADC").aggregate(
        adc_winrate=((Avg("win") * 100) - 49) / 2,
        adc_kda=(Avg("kills") + Avg("assists")) / Avg("deaths") - 2,
        adc_gold=(Avg("goldearned") / 1000 - 9.5) / 3,
        adc_timeliving=(Avg("longesttimespentliving") - 600) / 100,
        adc_cs=Avg("totminionskilled") / 200,
        adc_vision=Avg("visionscore") / 30,
        adc_lvl=(Avg("champlvl") - 10) / 8,
    )
    support = Data.objects.filter(position="SUPP").aggregate(
        support_winrate=((Avg("win") * 100) - 49) / 2,
        support_kda=(Avg("kills") + Avg("assists")) / Avg("deaths") - 2,
        support_gold=(Avg("goldearned") / 1000 - 9.5) / 3,
        support_timeliving=(Avg("longesttimespentliving") - 600) / 100,
        support_cs=Avg("totminionskilled") / 200,
        support_vision=Avg("visionscore") / 30,
        support_lvl=(Avg("champlvl") - 10) / 8,
    )
    if position is None:
        return dict(top=top, jungle=jungle, mid=mid, adc=adc, support=support)
    elif position == "TOP":
        return top
    elif position == "JUNGLE":
        return jungle
    elif position == "MID":
        return mid
    elif position == "ADC":
        return adc
    elif position == "SUPP":
        return support


def ChampWR():
    return [
        ["Ivern", 55.87, 8194],
        ["Anivia", 53.87, 7785],
        ["Xerath", 53.52, 6273],
        ["Sona", 53.44, 14090],
        ["Ahri", 53.31, 37423],
        ["Janna", 52.91, 24296],
        ["Skarner", 52.87, 2111],
        ["Pantheon", 52.49, 11305],
        ["Amumu", 52.4, 13584],
        ["Draven", 52.31, 20327],
        ["Warwick", 52.24, 19233],
        ["Twitch", 52.23, 22841],
        ["KogMaw", 52.23, 7871],
        ["Zilean", 52.2, 5943],
        ["Xin Zhao", 52.09, 15559],
        ["Annie", 52.07, 14454],
        ["Ziggs", 52.0, 8295],
        ["Yasuo", 51.67, 30257],
        ["Soraka", 51.64, 13721],
        ["Tryndamere", 51.63, 14630],
        ["Blitzcrank", 51.63, 23650],
        ["Master Yi", 51.51, 25683],
        ["Kayle", 51.5, 6373],
        ["Leona", 51.44, 19317],
        ["Miss Fortune", 51.41, 16453],
        ["Irelia", 51.39, 11422],
        ["Darius", 51.3, 18586],
        ["Brand", 51.13, 16019],
        ["Aatrox", 51.05, 4098],
        ["Teemo", 51.0, 14807],
        ["Jarvan IV", 50.98, 9029],
        ["Illaoi", 50.96, 6685],
        ["Caitlyn", 50.96, 57275],
        ["VelKoz", 50.94, 11007],
        ["Sejuani", 50.92, 11853],
        ["Swain", 50.92, 7333],
        ["Jax", 50.85, 20635],
        ["Kindred", 50.84, 3328],
        ["Riven", 50.83, 22019],
        ["Nunu", 50.81, 5355],
        ["Karthus", 50.75, 2853],
        ["Shaco", 50.74, 11714],
        ["Taric", 50.71, 3672],
        ["Lulu", 50.64, 24676],
        ["Vi", 50.63, 12245],
        ["Nami", 50.59, 17468],
        ["Jinx", 50.58, 27199],
        ["Wukong", 50.57, 7745],
        ["Bard", 50.55, 12308],
        ["Fiora", 50.42, 18899],
        ["Lucian", 50.38, 56676],
        ["Renekton", 50.34, 18676],
        ["Morgana", 50.34, 23280],
        ["Thresh", 50.33, 48877],
        ["Yorick", 50.28, 4423],
        ["Fiddlesticks", 50.26, 6227],
        ["Kassadin", 50.21, 15502],
        ["Sion", 50.18, 5197],
        ["Twisted Fate", 50.17, 9673],
        ["Hecarim", 50.13, 9527],
        ["Fizz", 50.1, 22139],
        ["Malphite", 50.07, 10523],
        ["Orianna", 50.01, 28594],
        ["Garen", 49.98, 9832],
        ["Kled", 49.93, 7801],
        ["Katarina", 49.84, 12786],
        ["Braum", 49.75, 14761],
        ["Syndra", 49.73, 18093],
        ["Zyra", 49.71, 11807],
        ["Nocturne", 49.69, 6039],
        ["Lux", 49.68, 27020],
        ["Shyvana", 49.68, 5411],
        ["Tristana", 49.67, 12858],
        ["Vayne", 49.64, 35014],
        ["Jayce", 49.61, 9879],
        ["Zac", 49.59, 11151],
        ["Rammus", 49.52, 5365],
        ["Talon", 49.5, 7470],
        ["Ashe", 49.46, 22988],
        ["Varus", 49.46, 9711],
        ["Ekko", 49.39, 19504],
        ["KhaZix", 49.34, 19531],
        ["Aurelion Sol", 49.26, 2231],
        ["Alistar", 49.24, 9127],
        ["Xayah", 49.2, 28944],
        ["Elise", 49.18, 14202],
        ["Volibear", 49.13, 5424],
        ["Evelynn", 49.13, 7671],
        ["Galio", 49.1, 13110],
        ["Gangplank", 49.07, 16859],
        ["Veigar", 49.06, 12298],
        ["Akali", 49.0, 10563],
        ["Sivir", 48.98, 6831],
        ["Singed", 48.88, 3216],
        ["Taliyah", 48.86, 5626],
        ["Heimerdinger", 48.84, 4150],
        ["Diana", 48.72, 6960],
        ["RekSai", 48.62, 2106],
        ["Maokai", 48.62, 13439],
        ["Gragas", 48.59, 21196],
        ["Olaf", 48.58, 6283],
        ["Karma", 48.56, 23927],
        ["Kalista", 48.53, 6767],
        ["Graves", 48.53, 23123],
        ["Lee Sin", 48.46, 59286],
        ["Nasus", 48.45, 10202],
        ["Mordekaiser", 48.41, 2107],
        ["Shen", 48.34, 10293],
        ["Corki", 48.33, 2390],
        ["ChoGath", 48.26, 7416],
        ["Rumble", 48.21, 7615],
        ["Viktor", 48.18, 6577],
        ["Lissandra", 48.16, 4483],
        ["Nautilus", 48.14, 13431],
        ["Quinn", 48.1, 3684],
        ["Vladimir", 48.09, 11661],
        ["Malzahar", 48.0, 5804],
        ["Udyr", 47.94, 4750],
        ["DrMundo", 47.92, 4017],
        ["Cassiopeia", 47.89, 6567],
        ["Tahm Kench", 47.75, 5229],
        ["Trundle", 47.63, 4239],
        ["Gnar", 47.55, 6114],
        ["Kennen", 47.28, 9066],
        ["Camille", 47.22, 4562],
        ["Nidalee", 46.76, 5597],
        ["Zed", 46.51, 21948],
        ["Poppy", 46.44, 6582],
        ["LeBlanc", 46.41, 10642],
        ["Jhin", 46.27, 13911],
        ["Urgot", 46.03, 1021],
        ["Rakan", 46.01, 21616],
        ["Rengar", 45.63, 8121],
        ["Ezreal", 45.61, 28397],
        ["Azir", 43.94, 3166],
        ["Ryze", 39.65, 5737],
    ]


def champData(champid):
    #################################################################################################
    # stats
    #################################################################################################

    champstatobj, created = ChampStats.objects.get_or_create(champ_id=champid)

    if (
        created
        or champstatobj.champ_winrate == 0
        or champstatobj.champ_kda == 0
        or champstatobj.champ_lvl == 0
    ):
        dict_stat = (
            Data.objects.filter(championid=champid)
            .exclude(deaths__lt=1)
            .aggregate(
                champ_winrate=Avg("win") * 100,
                champ_kda=(Avg("kills") + Avg("assists")) / Avg("deaths"),
                champ_lvl=Avg("champlvl"),
            )
        )
        champstatobj.champ_winrate = dict_stat["champ_winrate"]
        champstatobj.champ_kda = dict_stat["champ_kda"]
        champstatobj.champ_lvl = dict_stat["champ_lvl"]
        champstatobj.save()

    dict_stat = {
        "champ_winrate": champstatobj.champ_winrate,
        "champ_kda": champstatobj.champ_kda,
        "champ_lvl": champstatobj.champ_lvl,
    }

    if champstatobj.champ_dmgtype == "":
        ad_damage = Data.objects.filter(championid=champid).values_list(
            "physicaldmgdealt", flat=True
        )
        ap_damage = Data.objects.filter(championid=champid).values_list(
            "magicdmgdealt", flat=True
        )
        tot_ap_damage = 0
        tot_ad_damage = 0

        for i in range(len(ad_damage)):
            tot_ad_damage += ad_damage[i]

        for i in range(len(ap_damage)):
            tot_ap_damage += ap_damage[i]

        if len(ap_damage) != 0:
            tot_ap_damage /= len(ap_damage)
        if len(ad_damage) != 0:
            tot_ad_damage /= len(ad_damage)

        dmgtype = "AD" if tot_ad_damage > tot_ap_damage else "AP"

        champstatobj.champ_dmgtype = dmgtype
        champstatobj.save()

    dmgtype = champstatobj.champ_dmgtype

    dict_stat.update({"champ_dmgtype": dmgtype})
    dict_stat.update({"champ_dmgtype_icon": f"{dmgtype}.png"})
    dict_stat.update({"champ_name": Champs.objects.get(id=champid).name})
    dict_stat.update({"champ_id": champid})

    #################################################################################################
    # position
    #################################################################################################

    dict_pos = {}

    champ_stats = ChampStats.objects.get(champ_id=champid)
    champ_top_count = champ_stats.champ_top_count
    champ_jungle_count = champ_stats.champ_jungle_count
    champ_mid_count = champ_stats.champ_mid_count
    champ_adc_count = champ_stats.champ_adc_count
    champ_support_count = champ_stats.champ_support_count
    champ_count = champ_stats.champ_count

    dict_pos.update({"champ_top_count": champ_top_count})
    dict_pos.update({"champ_jungle_count": champ_jungle_count})
    dict_pos.update({"champ_mid_count": champ_mid_count})
    dict_pos.update({"champ_adc_count": champ_adc_count})
    dict_pos.update({"champ_support_count": champ_support_count})
    dict_pos.update({"champ_count": champ_count})

    #################################################################################################
    # items
    #################################################################################################

    def create_dict_item_occ(itemslot):
        list_item = list(
            Data.objects.filter(championid=champid).values_list(itemslot, flat=True)
        )
        set_item = set(list_item)
        dict_item_occ = {}
        for item in set_item:
            occ = list_item.count(item)
            dict_item_occ.update({item: occ})
        dict_item_occ = sorted(dict_item_occ.items(), key=lambda x: x[1], reverse=True)
        return dict_item_occ

    list_dict_items = [
        create_dict_item_occ("item1"),
        create_dict_item_occ("item2"),
        create_dict_item_occ("item3"),
        create_dict_item_occ("item4"),
        create_dict_item_occ("item5"),
        create_dict_item_occ("item6"),
    ]

    def delete_double(list_item):
        seen_values = {}
        added_in_seen_values = False

        for lst in list_item:
            while not added_in_seen_values:
                if lst[0][0] == 0 and len(lst) > 0:
                    lst.pop(0)
                if len(lst) > 0:
                    first_value = lst[0][0]
                    if first_value in seen_values:
                        lst.pop(0)
                    else:
                        seen_values[first_value] = True
                        added_in_seen_values = True
            added_in_seen_values = False

    delete_double(list_dict_items)
    most_frequent_items = [
        list_dict_items[0][0],
        list_dict_items[1][0],
        list_dict_items[2][0],
        list_dict_items[3][0],
        list_dict_items[4][0],
        list_dict_items[5][0],
    ]
    dict_item = {}
    slotindex = 1

    for item_id in most_frequent_items:
        try:
            item_object = Items.objects.get(id=item_id[0])
            item_name = item_object.name
            dict_item.update({f"Slot{slotindex}": item_name})
        except Items.DoesNotExist:
            dict_item.update({item_id[0]: "Item non trouvé"})
        slotindex += 1

    #################################################################################################
    # summoner spells
    #################################################################################################

    def create_dict_summ_occ(summspellslot):
        list_sum = list(
            Data.objects.filter(championid=champid).values_list(
                summspellslot, flat=True
            )
        )
        set_sum = set(list_sum)
        dict_sum_occ = {}
        for summspell in set_sum:
            occ = list_sum.count(summspell)
            dict_sum_occ.update({summspell: occ})
        dict_sum_occ = sorted(dict_sum_occ.items(), key=lambda x: x[1], reverse=True)
        return dict_sum_occ

    list_dict_summs = [create_dict_summ_occ("ss1"), create_dict_summ_occ("ss2")]
    delete_double(list_dict_summs)

    most_frequent_summ = [list_dict_summs[0][0], list_dict_summs[1][0]]
    dict_summ = {}
    slotindex = 1

    for summ_id in most_frequent_summ:
        try:
            summ_object = SummonerSpells.objects.get(id=summ_id[0])
            summ_name = summ_object.name
            dict_summ.update({f"Slot{slotindex}": summ_name})
        except SummonerSpells.DoesNotExist:
            dict_summ.update({summ_id[0]: "Summoner Spell non trouvé"})
        slotindex += 1

    #################################################################################################
    # image name
    #################################################################################################

    dict_img_name = {}
    slotindex = 1
    for itm in most_frequent_items:
        try:
            item_id = itm[0]
            item_name = Items.objects.get(id=item_id).name
            item_name = item_name.replace(":", "")
            dict_img_name[
                f"{item_name}"
            ] = f"{item_id}_{item_name.replace(' ', '-')}.png"

        except Items.DoesNotExist:
            dict_item.update({itm[0]: "Item non trouvé"})
            print(itm[0])
        slotindex += 1

    slotindex = 1

    for smm in most_frequent_summ:
        try:
            summ_id = smm[0]
            summ_name = SummonerSpells.objects.get(id=summ_id).name
            dict_img_name[
                f"{summ_name}"
            ] = f"{summ_id}_{summ_name.replace(' ', '-')}.png"
        except SummonerSpells.DoesNotExist:
            dict_summ.update({smm[0]: "Summoner Spell non trouvé"})
        slotindex += 1

    for slot, img_name in dict_img_name.items():
        if not os.path.exists(f"{absolute_path}/static/image_lol/{img_name}"):
            dict_img_name[slot] = "not_found.png"

    dict_img_name_champ = {}
    champ_name = Champs.objects.get(id=champid).name
    img_name = f"{champid}_{champ_name.replace(' ', '-')}.png"
    if not os.path.exists(f"{absolute_path}/static/image_lol/{img_name}"):
        dict_img_name_champ.update({"champ_icon": "not_found.png"})
        print("not found")
    else:
        dict_img_name_champ.update({"champ_icon": img_name})

    #################################################################################################
    # final dict
    #################################################################################################

    return dict(
        champ_stat=dict_stat,
        champ_pos=dict_pos,
        champ_item=dict_item,
        champ_sum=dict_summ,
        champ_img_name=dict_img_name,
        champ_img_name_champ=dict_img_name_champ,
    )


def get_champs():
    champlist = []
    for champ in Champs.objects.all():
        champ: Champs
        dict_champ = {}
        if not hasattr(champ, "champstats"):
            dict_pos = Data.objects.filter(championid=champ.id).aggregate(
                champ_top_count=Count("position", filter=Q(position="TOP")),
                champ_jungle_count=Count("position", filter=Q(position="JUNGLE")),
                champ_mid_count=Count("position", filter=Q(position="MID")),
                champ_adc_count=Count("position", filter=Q(position="ADC")),
                champ_support_count=Count("position", filter=Q(position="SUPP")),
                champ_count=Count("position"),
            )
            stats, created = ChampStats.objects.get_or_create(
                champ=champ,
                champ_top_count=dict_pos["champ_top_count"],
                champ_jungle_count=dict_pos["champ_jungle_count"],
                champ_mid_count=dict_pos["champ_mid_count"],
                champ_adc_count=dict_pos["champ_adc_count"],
                champ_support_count=dict_pos["champ_support_count"],
                champ_count=dict_pos["champ_count"],
            )
            stats.save()

        stats = champ.champstats

        top = stats.champ_top_count
        jungle = stats.champ_jungle_count
        mid = stats.champ_mid_count
        bot = stats.champ_adc_count
        support = stats.champ_support_count

        posocc = max(top, jungle, mid, bot, support)

        if posocc == top:
            pos = "Top"
        elif posocc == jungle:
            pos = "Jungle"
        elif posocc == mid:
            pos = "Mid"
        elif posocc == bot:
            pos = "Bot"
        elif posocc == support:
            pos = "Support"
        else:
            pos = "None"

        dict_champ.update({"champ_pos": pos})

        champ_name = champ.name
        img_name = f"{champ.id}_{champ_name.replace(' ', '-')}.png"
        if not os.path.exists(f"{absolute_path}/static/image_lol/{img_name}"):
            dict_champ.update({"champ_icon": static("image_lol/not_found.png")})
        else:
            dict_champ.update({"champ_icon": static(f"image_lol/{img_name}")})

        dict_champ.update({"champ_name": champ_name})
        dict_champ.update({"champ_id": champ.id})

        champlist.append(dict_champ)

    return champlist


def get_items_set(champid, max_nan_item=0):
    list_itemset = list(
        Data.objects.filter(championid=champid).values_list(
            "item1", "item2", "item3", "item4", "item5", "item6"
        )
    )
    list_itemset_sorted = []
    for itemset in list_itemset:
        itemset = list(itemset)
        zero_count = itemset.count(0)
        if zero_count == max_nan_item:
            itemset.sort(reverse=True)
            list_itemset_sorted.append(tuple(itemset))
    set_itemset = set(list_itemset_sorted)
    dict_set_itemset = {}

    ########################################### lent ################################################
    for item in set_itemset:
        occ = list_itemset_sorted.count(item)
        dict_set_itemset.update({item: occ})
    #################################################################################################

    dict_set_itemset = sorted(
        dict_set_itemset.items(), key=lambda x: x[1], reverse=True
    )

    return dict_set_itemset


"""    champstatobj, created = ChampStats.objects.get_or_create(champ_id=champid)

    if max_nan_item == 0:
        champ_data = champstatobj.champ_item_set_six_item
    elif max_nan_item == 1:
        champ_data = champstatobj.champ_item_set_five_item
    elif max_nan_item == 2:
        champ_data = champstatobj.champ_item_set_four_item
    elif max_nan_item == 3:
        champ_data = champstatobj.champ_item_set_three_item
    elif max_nan_item == 4:
        champ_data = champstatobj.champ_item_set_two_item
    else:
        champ_data = champstatobj.champ_item_set_one_item

    if created or champ_data == dict:
        list_itemset = list(Data.objects.filter(championid=champid).values_list('item1', 'item2', 'item3', 'item4', 'item5', 'item6'))
        list_itemset_sorted = []
        for itemset in list_itemset:
            itemset = list(itemset)
            zero_count = itemset.count(0)
            if zero_count == max_nan_item:
                itemset.sort(reverse=True)
                list_itemset_sorted.append(tuple(itemset))
        set_itemset = set(list_itemset_sorted)
        dict_set_itemset = {}
        for item in set_itemset:
            occ = list_itemset_sorted.count(item)
            dict_set_itemset.update({item: occ})
        dict_set_itemset = sorted(dict_set_itemset.items(), key=lambda x: x[1], reverse=True)
        json_set_itemset = json.dumps(dict_set_itemset)

        champ_data = json_set_itemset
        champstatobj.save()

    dict_set_itemset = json.loads(champ_data)

    return dict_set_itemset"""
