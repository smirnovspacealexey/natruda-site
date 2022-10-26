from django.contrib import admin
from .models import Point


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'address', 'volume', 'subnetwork', 'picture', 'ordering', ]
    list_editable = ('name', 'address', 'volume', 'picture', 'subnetwork', 'ordering', )


