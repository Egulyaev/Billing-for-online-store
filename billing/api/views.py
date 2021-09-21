from rest_framework import viewsets, mixins
from rest_framework.response import Response

from main.models import Promo, Promo
from api.serializers import PromoSerializer


class ListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class TicketViewSet(ListViewSet):
    serializer_class = PromoSerializer

    def list(self, request):
        queryset = Promo.objects.all()
        serializer = PromoSerializer(queryset, many=True)
        return Response(serializer.data)
