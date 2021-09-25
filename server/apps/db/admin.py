from django.contrib import admin

from .models import Measure, Point


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    pass


@admin.register(Point)
class MeasureAdmin(admin.ModelAdmin):
    pass
