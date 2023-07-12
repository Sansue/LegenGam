from django import forms
from graph.models import Champs


class ChooseChampForm(forms.Form):
    champ = forms.ModelChoiceField(
        queryset=Champs.objects.all().values_list("name", flat=True),
        widget=forms.Select(attrs={"class": "select2"}),
    )
