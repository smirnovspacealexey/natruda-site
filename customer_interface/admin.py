from django.contrib import admin

from .models import Menu, MacroProduct, ContentOption, ProductOption, ProductVariant, SizeOption, MacroProductContent

# Register your models here.


class MacroProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}


class MacroProductContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}

admin.site.register(Menu)
admin.site.register(MacroProduct, MacroProductAdmin)
admin.site.register(MacroProductContent, MacroProductContentAdmin)
admin.site.register(ContentOption)
admin.site.register(ProductOption)
admin.site.register(ProductVariant)
admin.site.register(SizeOption)
