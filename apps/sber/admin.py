from django.contrib import admin
from .models import SberSettings, SberSettingsForm


@admin.register(SberSettings)
class SberSettingsAdmin(admin.ModelAdmin):
    form = SberSettingsForm
    list_display = ['login', 'min_amount', 'max_amount', 'tax_system', 'in_test', 'active']
    list_editable = ('active', 'min_amount', 'max_amount', 'in_test', )


