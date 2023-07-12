from django.http import JsonResponse
from graph.champdata import ChampWR, statsbyposition
from graph.models import Data, Champs, Items


def dataset_manager(element):  # TODO
    if element == "champs_winrate":
        stats = ChampWR()
        return JsonResponse({"stats": stats, "chart_types": ["bar", "line"]})
    elif element == "top_stats":
        return Items.objects.all()
    elif element == "jungle_stats":
        return Data.objects.all()
    elif element == "mid_stats":
        return Data.objects.all()
    elif element == "adc_stats":
        return Data.objects.all()
    elif element == "supp_stats":
        return Data.objects.all()


"""
def chart_type_manager(element):  # TODO
    return None


def scale_manager(element, spec):  # TODO
    return None


def data_sort_manager(element, spec):  # TODO
    return None


def max_elem_manager(element):  # TODO
    return None
"""


def calcWinrateByChamp():
    database = Data.objects.all()
    champs = Champs.objects.all()
    results = []
    for champ in champs:
        name = champ.name
        wins = database.filter(win=1, championid=champ.id).count()
        losses = database.filter(win=0, championid=champ.id).count()
        winrate = 0
        if wins + losses > 0:
            winrate = wins / (wins + losses)
        results.append([name, winrate * 100, wins + losses])
    return results
