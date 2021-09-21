from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_purchase/',
         views.create_purchase,
         name='create_purchase'),
    path('day-purchases/',
         views.day_purchases_list,
         name='day_purchases_list'),
    path('promo-effect/',
         views.get_promo_effect_report,
         name='det_promo_effect_report'),
    path('promo-effect-product/',
         views.get_promo_effect_report_product,
         name='det_promo_effect_report_product'),
]
