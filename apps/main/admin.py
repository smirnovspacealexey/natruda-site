from django.contrib import admin
from .models import Point, Data, Image


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'address', 'volume', 'subnetwork', 'picture', 'ordering', ]
    list_editable = ('name', 'address', 'volume', 'picture', 'subnetwork', 'ordering', )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'picture', 'preview', 'mobile', 'ordering']
    list_editable = ('picture', 'ordering', 'mobile',)
    readonly_fields = ["preview"]
    prepopulated_fields = {"slug": ('title',)}


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ['pk', 'active', ]
    list_editable = ('active',)






