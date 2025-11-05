from rest_framework import serializers

from traders_commitment.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source="verbose_name")

    class Meta:
        model = Currency
        fields = ["name", "symbol"]
