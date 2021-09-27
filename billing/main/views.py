import csv

from django.db.models import Count, Prefetch
from django.db.models.functions import TruncDay
from django.http import HttpResponse
from django.shortcuts import render, redirect

from main.forms import GetDateForm, PurchasesForm
from main.models import Purchases, Promo


def index(request):
    """Главная страница"""
    return render(request, 'index.html')


def create_purchase(request):
    form = PurchasesForm(request.POST or None)
    if request.method == 'GET' or not form.is_valid():
        return render(
            request,
            'create_purchase.html',
            {'form': form}
        )
    purchase = form.save(commit=False)
    if purchase.product.promo.exists():  # select_related
        promo_id = purchase.product.promo.get().id
        purchase.promo_price = (purchase.product.price
                                - purchase.product.price / 100
                                * purchase.product.promo.get().percent)
        purchase.promo = Promo.objects.get(id=promo_id)
    elif purchase.product.category.promo.exists():
        promo_id = purchase.product.category.promo.get().id
        purchase.promo_price = (purchase.product.price
                                - purchase.product.price / 100
                                * purchase.product.category.promo.get().percent)
        purchase.promo = Promo.objects.get(id=promo_id)
    else:
        purchase.promo_price = purchase.product.price
    purchase.save()
    return redirect('index')


def day_purchases_list(request):
    """Создание CSV отчета, который показывает
    какие покупки были совершены за день"""
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment;'
                                        ' filename="day_purchases.csv"'},
    )
    if request.method == 'POST':
        form = GetDateForm(request.POST)
        if form.is_valid():
            purchases = Purchases.objects.select_related('product', 'promo').filter(buy_date=form.cleaned_data['purchase'])
            writer = csv.writer(response)
            writer.writerow(
                ['Дата и время покупки',
                 'Наименование товара',
                 'Цена',
                 'Наименование акции',
                 'Процент скидки']
            )
            for purchase in purchases:
                if purchase.promo:
                    writer.writerow(
                        [
                        purchase.buy_time,
                        purchase.product,
                        purchase.product.price,
                        purchase.promo.name,
                        purchase.promo.percent
                        ]
                    )
                else:
                    writer.writerow(
                            [purchase.buy_time,
                             purchase.product,
                             purchase.product.price, 0, 0]
                        )
            return response
    else:
        form = GetDateForm()
    return render(request, 'day_purchases_list.html', {'form': form})


def get_promo_effect_report(request):
    """Создание CSV отчета, который показывает эффективность
     скидочных акций для категорий"""
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment;'
                                        ' filename="promo_effect.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(
        ['Скидочная акция',
         'Имя категории',
         'Среднее число продаваемых товаров в день со скидкой',
         'Среднее число продаваемых товаров в день без скидки']
    )
    promo_purchase = Promo.objects.all().exclude(category__isnull=True).select_related('category').annotate(
        Count('promobuy__id', distinct=True),
        Count('promobuy__buy_date', distinct=True),
        Count('category__product__purchases__id', distinct=True)
    )
    for promo in promo_purchase:
        cnt_promo_buys = promo.promobuy__id__count
        days_promo_buys = promo.promobuy__buy_date__count
        avg_promo_buys = cnt_promo_buys / days_promo_buys
        cnt_not_promo_buys = promo.category__product__purchases__id__count - cnt_promo_buys
        avg_not_promo_buys = cnt_not_promo_buys / days_promo_buys
        writer.writerow(
            [
             promo.name,
             promo.category,
             avg_promo_buys,
             avg_not_promo_buys
             ]
        )
    return response


def get_promo_effect_report_product(request):
    """Создание CSV отчета, который показывает эффективность
    скидочных акций для товаров"""
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; '
                                        'filename="promo_effect_product.csv"'},
    )
    promos = Promo.objects.all().exclude(product__isnull=True).select_related('product').annotate(
        Count('promobuy__id', distinct=True),
        Count('promobuy__buy_date', distinct=True),
        Count('product__purchases__id', distinct=True)
    )
    writer = csv.writer(response)
    writer.writerow(
        ['Скидочная акция',
         'Имя товара',
         'Среднее число продаваемых товаров в день со скидкой',
         'Среднее число продаваемых товаров в день без скидки']
    )
    for promo in promos:
        cnt_promo_buys = promo.promobuy__id__count
        days_promo_buys = promo.promobuy__buy_date__count
        avg_promo_buys = cnt_promo_buys / days_promo_buys
        cnt_not_promo_buys = promo.product__purchases__id__count - cnt_promo_buys
        avg_not_promo_buys = cnt_not_promo_buys / days_promo_buys
        writer.writerow(
            [
                promo.name,
                promo.product,
                avg_promo_buys,
                avg_not_promo_buys
            ]
        )
    return response
