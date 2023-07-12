from django.db.models import Count
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponse,
)
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
import json
from graph.calc import *
from graph import champdata, champdata_ajax
from graph.formchampion import ChooseChampForm
from graph.models import Data, Champs, Items
import csv
import concurrent.futures
from graph.ajax_graph_html_renderer import get_html


class HomeView(ListView):
    model = Data
    template_name = "index/home.html"
    context_object_name = "data"


def winrate(request):
    return render(
        request,
        "index/winratelastgames.html",
        {
            "wins": Data.objects.filter(win=1).count(),
            "losses": Data.objects.filter(win=0).count(),
        },
    )


def winrateByChamp(request):
    winrates = champdata.ChampWR()
    return render(request, "index/winratebychamp.html", {"winrates": winrates})


def winrateByChampGraph(request):
    winrates = champdata.ChampWR()
    return render(request, "index/champWR.html", {"data": winrates})


def statsbyposition(request):
    stats = champdata.statsbyposition()
    return render(request, "index/statsbyposition.html", {"data": stats})


def statsbypositionwithchoice(request):
    stats = champdata.statsbyposition()
    return render(request, "index/posstatswithchoice.html", {"data": stats})


def statsbychamp(request, champ):
    stats = champdata.champData(champ)
    return render(request, "index/champGuide.html", {"data": stats})


def formchampion(request):
    form = ChooseChampForm()

    if request.method == "POST":
        champobject = Champs.objects.get(name=request.POST.get("champ"))
        statsbychamp(request, champobject.id)
        return redirect(reverse("graph:statsbychamp", args=(champobject.id,)))

    return render(request, "index/formchampion.html", {"form": form})


def formchampionupdated(request):
    stats = champdata.get_champs()
    return render(request, "index/formchampionupdated.html", {"stats": stats})


def ajax_graph_render(request):
    return render(request, "index/ajax_graph.html")


@csrf_exempt
def ajax_graph_manager(request):
    element = request.POST.get("element")
    result = None
    if element == "champs_winrate":
        stats = ChampWR()
        result = JsonResponse({"stats": stats, "chart_types": ["bar", "line", "pie"]})
    elif element == "position_stats":
        stats = champdata.statsbyposition()
        result = JsonResponse({"stats": stats, "chart_types": ["radar", "bar"]})
    elif element == "cenareo_stats":
        stats = json.load(open("graph/static/cenareo_stats.json"))
        result = JsonResponse(
            {"stats": stats["values"], "chart_types": ["doughnut", "bar"]}
        )
    return result

@csrf_exempt
def ajax_graph_html_manager(request):
    i = request.POST.get("i")
    html_type = request.POST.get("html_type")  # only 'base' exists as of right now
    html = get_html(html_type, i)
    return JsonResponse({"html": html})


def search_champ_basehtml(request):
    query = request.GET.get("query", "")

    champions = Champs.objects.filter(name__icontains=query)

    champion_list = []
    for champion in champions:
        champion_data = {"id": champion.id, "name": champion.name}
        champion_list.append(champion_data)

    if len(champion_list) == 0:
        champion_list.append({"id": 0, "name": "No champion found"})

    response = {"champions": champion_list}

    return JsonResponse(response)


@csrf_exempt
def item_set_render(request):
    if request.method == "POST":
        value = request.POST.get("value")
        champid = request.POST.get("champid")
        response_data = []
        data = champdata.get_items_set(int(champid), int(value))[:3]

        for elm in data:
            elm_list = []
            for id_item in elm[0]:
                elm_list.append(id_item)

            for i in range(len(elm_list)):
                if elm_list[i] != 0:
                    try:
                        elm_list[i] = {
                            int(elm_list[i]): Items.objects.get(id=int(elm_list[i]))
                            .name.replace(" ", "-")
                            .replace(":", "")
                        }
                    except Items.DoesNotExist:
                        elm_list[i] = {
                            int(elm_list[i]): f"Item {elm_list[i]} not found"
                        }
                else:
                    elm_list[i] = {"None": "No item"}

            item_set = {
                "item_set": tuple(elm_list),
            }
            response_data.append(item_set)

        return HttpResponse(template_item_set_render(request, response_data))


def template_item_set_render(request, item_set):
    all_set = []

    for elm in item_set:
        data_item_set = []
        for item in elm["item_set"]:
            for key, value in item.items():
                if value == f"Item {key} not found":
                    data_item_set.append(
                        {
                            "item_id": key,
                            "item_name": value,
                            "item_img_name": "not_found.png",
                        }
                    )
                else:
                    if key != "None":
                        data_item_set.append(
                            {
                                "item_id": key,
                                "item_name": value,
                                "item_img_name": f"{key}_{value}.png",
                            }
                        )
                    else:
                        data_item_set.append(
                            {
                                "item_id": key,
                                "item_name": value,
                                "item_img_name": "no_item.png",
                            }
                        )
        all_set.append(data_item_set)

    return render(request, "index/template_item_set.html", {"item_set": all_set})


def statbychamp_ajax(request):
    return render(request, "index/champGuide_ajax.html")


@csrf_exempt
def update_positions(request):
    if request.method == "POST":
        positions = request.POST.get("positions")

        win_filter = request.POST.get("stateName")

        champion_name = request.POST.get("championName")

        positions = positions.split(",")

        for i in range(len(positions)):
            if positions[i] == "botlane":
                positions[i] = "ADC"
            elif positions[i] == "midlane":
                positions[i] = "MID"
            elif positions[i] == "toplane":
                positions[i] = "TOP"
            elif positions[i] == "jungle":
                positions[i] = "JUNGLE"
            elif positions[i] == "support":
                positions[i] = "SUPP"

        if win_filter == "win":
            win = 1
        elif win_filter == "lose":
            win = 0
        else:
            win = 2

        try:
            champion_id = Champs.objects.get(name=champion_name).id
        except Champs.DoesNotExist:
            champion_id = 0

        # renvoyer a un template
        fetched_data = {"positions": positions, "win": win, "champion_id": champion_id}

        champion_id = int(fetched_data["champion_id"])
        positions = fetched_data["positions"]
        win = int(fetched_data["win"])

        num_threads = 6
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)

        winrate_future = executor.submit(
            champdata_ajax.champdata_ajax_winrate, champion_id, positions
        )
        items_future = executor.submit(
            champdata_ajax.most_common_item, champion_id, positions, win
        )
        position_future = executor.submit(
            champdata_ajax.most_common_position, champion_id, win
        )
        kda_future = executor.submit(
            champdata_ajax.kda_ratio, champion_id, positions, win
        )
        images_future = executor.submit(
            champdata_ajax.items_images, items_future.result()
        )
        name_future = executor.submit(champdata_ajax.champinfo, champion_id)

        data_winrate = winrate_future.result()
        data_items = items_future.result()
        data_positions = position_future.result()
        data_kda = kda_future.result()
        data_image = images_future.result()
        data_name = name_future.result()

        updated_dict_pos = data_positions.copy()
        data_labels = []

        # Suppression des clés qui ne sont pas présentes dans la liste
        if fetched_data["positions"] != [""]:
            for key in data_positions.keys():
                if key not in fetched_data["positions"]:
                    updated_dict_pos[key] = 0
                else:
                    data_labels.append(key)
        else:
            data_labels = ["TOP", "JUNGLE", "MID", "ADC", "SUPP"]

        values_list = list(updated_dict_pos.values())[:-1]  # Exclude the last value

        # Calcul de la somme des valeurs du dictionnaire
        champ_count = sum(values_list)

        # Ajout du champ champ_count au dictionnaire
        updated_dict_pos["champ_count"] = champ_count

        data_chart = {
            "winrate": data_winrate,
            "dict_items": data_items,
            "positions": updated_dict_pos,
            "kda": data_kda,
            "images": data_image,
            "labels_chart": data_labels,
            "dict_name": data_name,
        }

        executor.shutdown()

        return JsonResponse(data_chart)


def importdata():
    i = 0
    with open("/Users/ethan/Desktop/DataMerge/merged_data.csv", newline="") as csvfile:
        data = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in data:
            if i == 0:
                i = 1
            else:
                typed_row = []
                for col in row:
                    try:
                        col = int(col)
                    except ValueError:
                        col = str(col)
                    typed_row.append(col)
                Data.objects.create(
                    championid=typed_row[0],
                    ss1=typed_row[1],
                    ss2=typed_row[2],
                    role=typed_row[3],
                    position=typed_row[4],
                    win=typed_row[5],
                    item1=typed_row[6],
                    item2=typed_row[7],
                    item3=typed_row[8],
                    item4=typed_row[9],
                    item5=typed_row[10],
                    item6=typed_row[11],
                    trinket=typed_row[12],
                    kills=typed_row[13],
                    deaths=typed_row[14],
                    assists=typed_row[15],
                    largestkillingspree=typed_row[16],
                    largestmultikill=typed_row[17],
                    killingsprees=typed_row[18],
                    longesttimespentliving=typed_row[19],
                    doublekills=typed_row[20],
                    triplekills=typed_row[21],
                    quadrakills=typed_row[22],
                    pentakills=typed_row[23],
                    legendarykills=typed_row[24],
                    totdmgdealt=typed_row[25],
                    magicdmgdealt=typed_row[26],
                    physicaldmgdealt=typed_row[27],
                    truedmgdealt=typed_row[28],
                    largestcrit=typed_row[29],
                    totdmgtochamp=typed_row[30],
                    magicdmgtochamp=typed_row[31],
                    physdmgtochamp=typed_row[32],
                    truedmgtochamp=typed_row[33],
                    totheal=typed_row[34],
                    totunitshealed=typed_row[35],
                    dmgselfmit=typed_row[36],
                    dmgtoobj=typed_row[37],
                    dmgtoturrets=typed_row[38],
                    visionscore=typed_row[39],
                    timecc=typed_row[40],
                    totdmgtaken=typed_row[41],
                    magicdmgtaken=typed_row[42],
                    physdmgtaken=typed_row[43],
                    truedmgtaken=typed_row[44],
                    goldearned=typed_row[45],
                    goldspent=typed_row[46],
                    turretkills=typed_row[47],
                    inhibkills_x=typed_row[48],
                    totminionskilled=typed_row[49],
                    neutralminionskilled=typed_row[50],
                    ownjunglekills=typed_row[51],
                    enemyjunglekills=typed_row[52],
                    totcctimedealt=typed_row[53],
                    champlvl=typed_row[54],
                    pinksbought=typed_row[55],
                    wardsbought=typed_row[56],
                    wardsplaced=typed_row[57],
                    wardskilled=typed_row[58],
                    firstblood=typed_row[59],
                    firsttower=typed_row[60],
                    firstinhib=typed_row[61],
                    firstbaron=typed_row[62],
                    firstdragon=typed_row[63],
                    firstharry=typed_row[64],
                    towerkills=typed_row[65],
                    inhibkills_y=typed_row[66],
                    baronkills=typed_row[67],
                    dragonkills=typed_row[68],
                    harrykills=typed_row[69],
                )
        print("end")
