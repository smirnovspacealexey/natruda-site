from django.contrib import admin

from .models import Menu, MacroProduct, ContentOption, ProductOption, ProductVariant, SizeOption, MacroProductContent, Order


# Register your models here.

class MacroProductContentInline(admin.TabularInline):
    model = MacroProductContent
    extra = 0


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 0


class MacroProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = ('title', 'customer_appropriate', 'ordering')
    list_editable = ('customer_appropriate', 'ordering')
    inlines = [MacroProductContentInline, ProductVariantInline]


class MacroProductContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    inlines = [ProductVariantInline]


class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer_title', 'weight', 'price', 'note', 'customer_appropriate')
    list_editable = ('customer_title', 'weight', 'price', 'note', 'customer_appropriate')
    inlines = [ProductVariantInline, ProductOptionInline]


admin.site.register(Order)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MacroProduct, MacroProductAdmin)
admin.site.register(MacroProductContent, MacroProductContentAdmin)
admin.site.register(ContentOption)
admin.site.register(ProductOption)
admin.site.register(ProductVariant)
admin.site.register(SizeOption)

