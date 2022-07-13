from django.contrib import admin

from .models import Menu, MacroProduct, ContentOption, ProductOption, ProductVariant, SizeOption, MacroProductContent


# Register your models here.


class MacroProductContentInline(admin.TabularInline):
    model = MacroProductContent
    extra = 0


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0


class MacroProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = ('title', 'customer_appropriate', 'ordering')
    list_editable = ('customer_appropriate', 'ordering')
    inlines = [MacroProductContentInline, ProductVariantInline]


class MacroProductContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}


admin.site.register(Menu)
admin.site.register(MacroProduct, MacroProductAdmin)
admin.site.register(MacroProductContent, MacroProductContentAdmin)
admin.site.register(ContentOption)
admin.site.register(ProductOption)
admin.site.register(ProductVariant)
admin.site.register(SizeOption)
