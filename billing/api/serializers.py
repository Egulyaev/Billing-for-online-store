from rest_framework import serializers


class DateSerializer(serializers.Serializer):
    date = serializers.DateField()


class DayReportResponseSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    product_name = serializers.CharField()
    product_price = serializers.IntegerField()
    promo_name = serializers.CharField()
    promo_percent = serializers.IntegerField()
