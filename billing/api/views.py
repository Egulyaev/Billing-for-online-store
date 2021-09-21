from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import DateSerializer, DayReportResponseSerializer
from main.models import Purchases


class DayReportResponse:
    def __init__(self, date, product_name,
                 product_price, promo_name, promo_percent):
        self.date = date
        self.product_name = product_name
        self.product_price = product_price
        self.promo_name = promo_name
        self.promo_percent = promo_percent


@api_view(['POST'])
def day_purchases_list_api(request):
    serializer = DateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    purchases = Purchases.objects. \
        filter(buy_date=serializer.validated_data['date'])
    results = []
    for purchase in purchases:
        if purchase.product.promo.exists():
            report = DayReportResponse(
                purchase.buy_time,
                purchase.product,
                purchase.product.price,
                purchase.product.promo.get(),
                purchase.product.promo.get().percent
            )
            serializer = DayReportResponseSerializer(report)
            results.append(serializer.data)
        elif purchase.product.category.promo.exists():
            report = DayReportResponse(
                 purchase.buy_time,
                 purchase.product,
                 purchase.product.price,
                 purchase.product.category.promo.get(),
                 purchase.product.category.promo.get().percent
            )
            serializer = DayReportResponseSerializer(report)
            results.append(serializer.data)
        else:
            report = DayReportResponse(
                 purchase.buy_time,
                 purchase.product,
                 purchase.product.price, 0, 0
            )
            serializer = DayReportResponseSerializer(report)
            results.append(serializer.data)
    return Response(results)
