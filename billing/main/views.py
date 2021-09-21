import csv

from django.db.models import Count
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
        purchase.promo_price = (purchase.product.price
                                - purchase.product.price / 100
                                * purchase.product.promo.get().percent)
    elif purchase.product.category.promo.exists():
        purchase.promo_price = (purchase.product.price
                                - purchase.product.price / 100
                                * purchase.product.category.promo.get().percent)
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
            purchases = Purchases.objects. \
                filter(buy_date=form.cleaned_data['purchase'])
            writer = csv.writer(response)
            writer.writerow(
                ['Дата покупки',
                 'Наименование товара',
                 'Цена',
                 'Наименование акции',
                 'Процент скидки']
            )
            for purchase in purchases:
                if purchase.product.promo.exists():
                    writer.writerow(
                        [purchase.buy_date,
                         purchase.product,
                         purchase.product.price,
                         purchase.product.promo.get(),
                         purchase.product.promo.get().percent]
                    )
                elif purchase.product.category.promo.exists():
                    writer.writerow(
                        [purchase.buy_date,
                         purchase.product,
                         purchase.product.price,
                         purchase.product.category.promo.get(),
                         purchase.product.category.promo.get().percent]
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
    promos = Promo.objects.all().exclude(category__isnull=True)
    writer = csv.writer(response)
    writer.writerow(
        ['Скидочная акция',
         'Имя категории',
         'Среднее число продаваемых товаров в день со скидкой',
         'Среднее число продаваемых товаров в день без скидки']
    )

    for promo in promos:
        days_count = Purchases.objects. \
            filter(product__category__promo=promo). \
            annotate(day=TruncDay('buy_date')). \
            values('day'). \
            annotate(count_purchase=Count('id')). \
            order_by('day').count()
        purchases_count = Purchases.objects. \
            filter(product__category__promo=promo).count()
        purchases_promo = purchases_count / days_count
        purchases = Purchases.objects.all().exclude(
            product__category__promo=promo).count() / days_count
        writer.writerow(
            [promo.name,
             promo.category,
             purchases_promo,
             purchases]
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
    promos = Promo.objects.all().exclude(product__isnull=True)
    writer = csv.writer(response)
    writer.writerow(
        ['Скидочная акция',
         'Имя товара',
         'Среднее число продаваемых товаров в день со скидкой',
         'Среднее число продаваемых товаров в день без скидки']
    )
    for promo in promos:
        days_count = Purchases.objects. \
            filter(product__promo=promo). \
            annotate(day=TruncDay('buy_date')). \
            values('day'). \
            annotate(count_purchase=Count('id')). \
            order_by('day').count()
        purchases_count = Purchases. \
            objects.filter(product__promo=promo). \
            count()
        purchases_promo = purchases_count / days_count
        purchases = Purchases.objects.all().exclude(
            product__promo=promo).count() / days_count
        writer.writerow(
            [promo.name, promo.product, purchases_promo, purchases]
        )
    return response
