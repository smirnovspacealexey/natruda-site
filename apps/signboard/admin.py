from django.contrib import admin
from .models import Signboard


@admin.register(Signboard)
class SignboardAdmin(admin.ModelAdmin):
    list_display = ['slug', 'active', 'signboard_url']
    list_editable = ('active', )
