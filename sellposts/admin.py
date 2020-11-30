from django.contrib import admin
from .models import *


class ImageStacked(admin.StackedInline):
    model = AdImages

class SellAdAdmin(admin.ModelAdmin):
    model = SellAd
    list_display = ['title', 'category', ]
    inlines = [ImageStacked]


admin.site.register(SellAd, SellAdAdmin)
