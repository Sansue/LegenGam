from django.contrib.auth.decorators import login_required
from django.urls import path
from graph.views import *

app_name = "graph"


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("winrate/", winrate, name="winrate"),
    path("winratebychamp/", winrateByChamp, name="winratebychamp"),
    path("winratebychampgraph/", winrateByChampGraph, name="winratebychampgraph"),
    path("statsbyposition/", statsbyposition, name="statsbyposition"),
    path("statsbypositionwithchoice/", statsbypositionwithchoice, name="statsbypositionwithchoice"),
    path("formchampion/", formchampion, name="formchampion"),
    path("statsbychamp/<int:champ>/", statsbychamp, name="statsbychamp"),
    path("formchampion_updated/", formchampionupdated, name="formchampionupdated"),
    path("ajax_graph/get_data/", ajax_graph_manager, name="get_data"),
    path("ajax_graph/get_html/", ajax_graph_html_manager, name="get_html"),
    path("getchampbase/", search_champ_basehtml, name="getchampbase"),
    path("ajax_graph/", ajax_graph_render, name="ajax_graph"),
    path("item_set/", item_set_render, name="item_set"),
    path("template_item_set/", template_item_set_render, name="template_item_set"),
    path("statbychamp_ajax/", statbychamp_ajax, name="statbychamp_ajax"),
    path("position_statbychamp_ajax/", update_positions, name="position_statbychamp_ajax"),
]
