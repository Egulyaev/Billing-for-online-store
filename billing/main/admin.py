from django.contrib import admin

from main.models import Category, Product, Promo, Purchases


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    empty_value_display = '-пусто-'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'category')
    empty_value_display = '-пусто-'


class PromoAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'category', 'product')
    empty_value_display = '-пусто-'


class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('buy_time', 'product', 'buyer')
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Promo, PromoAdmin)
admin.site.register(Purchases, PurchasesAdmin)
