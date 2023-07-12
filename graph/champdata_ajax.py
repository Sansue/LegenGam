import json
from django.db.models import Avg, When, Case, Value, Q, Count, F
from django.templatetags.static import static
from graph.models import Data, Champs, Items, SummonerSpells, ChampStats
import os, random

# filtrer par champion, par position, par win ou lose ou les deux, par item / item set ?
# ajouter classe du champion pour trier par class (ex marksman ...)


def champdata_ajax_winrate(champid=0, position=[]):
    # champid=0 means all champs
    # position=[] means no position selected so we take all
    if champid == 0:
        if position == [""]:
            winrate = Data.objects.all().aggregate(winrate=Avg("win") * 100)
        else:
            winrate = Data.objects.filter(position__in=position).aggregate(
                winrate=Avg("win") * 100
            )

    else:
        if position == [""]:
            winrate = Data.objects.filter(championid=champid).aggregate(
                winrate=Avg("win") * 100
            )
        else:
            winrate = Data.objects.filter(
                championid=champid, position__in=position
            ).aggregate(winrate=Avg("win") * 100)

    return winrate


def create_list_item(itemslot, champid, position, win):
    if champid == 0:
        if win == 2:
            if position == [""]:
                list_item = list(Data.objects.all().values_list(itemslot, flat=True))
            else:
                list_item = list(
                    Data.objects.filter(position__in=position).values_list(
                        itemslot, flat=True
                    )
                )

        else:
            if position == [""]:
                list_item = list(
                    Data.objects.filter(win=win).values_list(itemslot, flat=True)
                )
            else:
                list_item = list(
                    Data.objects.filter(position__in=position, win=win).values_list(
                        itemslot, flat=True
                    )
                )

        return create_dict_item_occ(list_item)

    else:
        if win == 2:
            if position == [""]:
                list_item = list(
                    Data.objects.filter(championid=champid).values_list(
                        itemslot, flat=True
                    )
                )
            else:
                list_item = list(
                    Data.objects.filter(
                        championid=champid, position__in=position
                    ).values_list(itemslot, flat=True)
                )

        else:
            if position == [""]:
                list_item = list(
                    Data.objects.filter(championid=champid, win=win).values_list(
                        itemslot, flat=True
                    )
                )
            else:
                list_item = list(
                    Data.objects.filter(
                        championid=champid, position__in=position, win=win
                    ).values_list(itemslot, flat=True)
                )

        return create_dict_item_occ(list_item)


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


def create_dict_item_occ(list_item):
    set_item = set(list_item)
    dict_item_occ = {}
    for item in set_item:
        occ = list_item.count(item)
        dict_item_occ.update({item: occ})
    dict_item_occ = sorted(dict_item_occ.items(), key=lambda x: x[1], reverse=True)
    return dict_item_occ


def most_common_item(champid=0, position=[""], win=2):
    list_dict_items = [
        create_list_item("item1", champid, position, win),
        create_list_item("item2", champid, position, win),
        create_list_item("item3", champid, position, win),
        create_list_item("item4", champid, position, win),
        create_list_item("item5", champid, position, win),
        create_list_item("item6", champid, position, win),
    ]

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

    return dict_item


def items_images(item_dict):
    dict_img_name = {}
    for itm in item_dict.items():
        try:
            item_name = itm[1]
            try:
                item_id = Items.objects.get(name=item_name).id
            except Items.MultipleObjectsReturned:
                item_id = Items.objects.filter(name=item_name).first().id
            item_name = item_name.replace(":", "")
            item_name = item_name.replace(" ", "-")
            image_name = f"{item_id}_{item_name}.png"
            dict_img_name.update({itm[1]: image_name})

        except Items.DoesNotExist:
            dict_img_name.update({itm[1]: "Item non trouvé"})

    return dict_img_name


def most_common_position(champid=0, win=2):
    if champid == 0:
        if win == 2:
            dict_pos = Data.objects.filter().aggregate(
                TOP=Count("position", filter=Q(position="TOP")),
                JUNGLE=Count("position", filter=Q(position="JUNGLE")),
                MID=Count("position", filter=Q(position="MID")),
                ADC=Count("position", filter=Q(position="ADC")),
                SUPP=Count("position", filter=Q(position="SUPP")),
                champ_count=Count("position"),
            )
        else:
            dict_pos = Data.objects.filter(win=win).aggregate(
                TOP=Count("position", filter=Q(position="TOP")),
                JUNGLE=Count("position", filter=Q(position="JUNGLE")),
                MID=Count("position", filter=Q(position="MID")),
                ADC=Count("position", filter=Q(position="ADC")),
                SUPP=Count("position", filter=Q(position="SUPP")),
                champ_count=Count("position"),
            )

    else:
        if win == 2:
            dict_pos = Data.objects.filter(championid=champid).aggregate(
                TOP=Count("position", filter=Q(position="TOP")),
                JUNGLE=Count("position", filter=Q(position="JUNGLE")),
                MID=Count("position", filter=Q(position="MID")),
                ADC=Count("position", filter=Q(position="ADC")),
                SUPP=Count("position", filter=Q(position="SUPP")),
                champ_count=Count("position"),
            )
        else:
            dict_pos = Data.objects.filter(championid=champid, win=win).aggregate(
                TOP=Count("position", filter=Q(position="TOP")),
                JUNGLE=Count("position", filter=Q(position="JUNGLE")),
                MID=Count("position", filter=Q(position="MID")),
                ADC=Count("position", filter=Q(position="ADC")),
                SUPP=Count("position", filter=Q(position="SUPP")),
                champ_count=Count("position"),
            )

    return dict_pos


def kda_ratio(champid=0, position=[], win=2):
    if champid == 0:
        if win == 2:
            if position == [""]:
                dict_kda = Data.objects.all().aggregate(
                    kda=(Avg("kills") + Avg("assists")) / Avg("deaths")
                )
            else:
                dict_kda = Data.objects.filter(position__in=position).aggregate(
                    kda=(Avg("kills") + Avg("assists")) / Avg("deaths")
                )

        else:
            if position == [""]:
                dict_kda = Data.objects.filter(win=win).aggregate(
                    kda=(Avg("kills") + Avg("assists")) / Avg("deaths")
                )
            else:
                dict_kda = Data.objects.filter(
                    position__in=position, win=win
                ).aggregate(kda=(Avg("kills") + Avg("assists")) / Avg("deaths"))

    else:
        if win == 2:
            if position == [""]:
                dict_kda = Data.objects.filter(championid=champid).aggregate(
                    kda=(Avg("kills") + Avg("assists")) / Avg("deaths")
                )
            else:
                dict_kda = Data.objects.filter(
                    championid=champid, position__in=position
                ).aggregate(kda=(Avg("kills") + Avg("assists")) / Avg("deaths"))

        else:
            if position == [""]:
                dict_kda = Data.objects.filter(championid=champid, win=win).aggregate(
                    kda=(Avg("kills") + Avg("assists")) / Avg("deaths")
                )
            else:
                dict_kda = Data.objects.filter(
                    championid=champid, position__in=position, win=win
                ).aggregate(kda=(Avg("kills") + Avg("assists")) / Avg("deaths"))

    return dict_kda


def champinfo(champid=0):
    if champid == 0:
        dict_champ_info = {
            "champname": "All champs",
            "champimgname": "All.png",
        }
    else:
        champname = Champs.objects.get(id=champid).name
        champname = champname.replace(" ", "-")
        champname = champname.replace(":", "")
        champimgname = f"{champid}_{champname}.png"
        dict_champ_info = {"champname": champname, "champimgname": champimgname}
    return dict_champ_info
