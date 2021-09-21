from datetime import datetime

from rest_framework import serializers

from main.models import Promo


class PromoSerializer(serializers.ModelSerializer):
    current_date=serializers.DateTimeField(default=datetime.now())

    class Meta:
        fields = '__all__'
        model = Promo