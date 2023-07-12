from django.contrib import admin
from .models import Data


class DataAdmin(admin.ModelAdmin):
    list_display = ("championid", "position")


admin.site.register(Data, DataAdmin)
