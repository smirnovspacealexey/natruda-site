from django.contrib import admin
from django.utils.html import format_html
from .models import Menu, MacroProduct, ContentOption, ProductOption, ProductVariant, SizeOption, MacroProductContent,\
    Order, get_html_img


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
    list_display = ('title', 'picture', 'preview', 'ordering', 'with_content', 'customer_appropriate')
    list_editable = ('customer_appropriate', 'picture', 'ordering')

    fieldsets = (
        (None, {
            'fields': ['title', 'customer_title', 'slug', 'internal_id', 'customer_appropriate', 'ordering']
        }),
        ('Картинка', {
            'fields': ('picture', 'preview')
        }),
    )
    inlines = [MacroProductContentInline, ProductVariantInline]
    readonly_fields = ["preview"]

    def preview(self, obj):
        return get_html_img(obj.picture)


class MacroProductContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    inlines = [ProductVariantInline]

    list_display = ('title', 'customer_title', 'internal_id', 'picture', 'preview', 'customer_appropriate', 'customer_description')
    list_editable = ('customer_title', 'customer_description', 'customer_appropriate', 'picture')
    readonly_fields = ["preview"]

    fieldsets = (
        (None, {
            'fields': ['title', 'customer_title', 'customer_description', 'slug', 'content_option', 'macro_product', 'internal_id', 'customer_appropriate']
        }),
        ('Картинка', {
            'fields': ('picture', 'preview')
        }),
    )

    def preview(self, obj):
        return get_html_img(obj.picture)


class MenuAdmin(admin.ModelAdmin):     # customer_appropriate скрыто. так как не обрабатывается пока ещё в коде
    list_display = ('__str__', 'customer_title', 'weight', 'price', 'icon', 'preview', 'customer_appropriate', 'note')
    list_editable = ('customer_title', 'weight', 'price', 'icon', 'customer_appropriate')
    inlines = [ProductVariantInline, ProductOptionInline]
    readonly_fields = ["preview"]

    search_fields = ['title', 'customer_title', 'weight', 'price']
    list_filter = ['is_by_weight']

    def preview(self, obj):
        return get_html_img(obj.icon)


class ContentOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer_title', 'internal_id', 'picture', 'preview')
    list_editable = ('customer_title', 'picture')
    readonly_fields = ["preview"]

    fieldsets = (
        (None, {
            'fields': ['title', 'customer_title', 'internal_id']
        }),
        ('Картинка', {
            'fields': ('picture', 'preview')
        }),
    )

    def preview(self, obj):
        return get_html_img(obj.picture)


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer_title', 'internal_id')


class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer_title', 'internal_id')
    filter_horizontal = ('product_variants', )
    autocomplete_fields = ['menu_item']


admin.site.register(Order)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MacroProduct, MacroProductAdmin)
admin.site.register(MacroProductContent, MacroProductContentAdmin)
admin.site.register(ContentOption, ContentOptionAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)
admin.site.register(SizeOption)

