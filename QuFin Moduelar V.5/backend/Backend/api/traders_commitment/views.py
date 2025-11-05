from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from traders_commitment.models import Currency, CoTFin, CurrencyValue
from .serializers import CurrencySerializer


class CurrenciesViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer



class COTDataViewSet(GenericViewSet, mixins.ListModelMixin):
    renderer_classes = [JSONRenderer]

    def list(self, request):
        name = request.query_params.get("name", None)
        if name is None:
            return Response({"error": "Provide `name` query param"}, status=status.HTTP_400_BAD_REQUEST)

        currency = Currency.objects.filter(name=name).first()

        if currency is None:
            return Response({"error": "Currency is not found"}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            "currencyData": [],
            "cotData": [],
        }

        currency_values = CurrencyValue.objects.prefetch_related("currency").filter(currency=currency)
        cot_data = CoTFin.objects.prefetch_related("currency").filter(currency=currency)

        for currency_value in currency_values:
            response_data["currencyData"].append({
                "date": currency_value.timestamp,
                "openPrice": currency_value.open_price,
                "closePrice": currency_value.close_price,
                "highPrice": currency_value.high_price,
                "lowPrice": currency_value.low_price,
                "adjClosePrice": currency_value.adj_close_price,
            })

        
        for item in cot_data:
            response_data["cotData"].append({
                "date": item.date,
                "assetManagerPositionsLong": item.asset_manager_positions_long,
                "assetManagerPositionsShort": item.asset_manager_positions_short,
                "assetManagerPositionsLongShort": item.asset_manager_positions_long_short,

                "leverageMoneyPositionsLong": item.leverage_money_positions_long,
                "leverageMoneyPositionsShort": item.leverage_money_positions_short,
                "leverageMoneyPositionsLongShort": item.leverage_money_positions_long_short,

                "otherReptPositionsLongAll": item.other_rept_positions_long_all,
                "otherReptPositionsShortAll": item.other_rept_positions_short_all,
                "otherReptPositionsLongShortAll": item.other_rept_positions_long_short_all,

                "percentageOfOpenInterestAssetManagerLong": item.percentage_of_open_interest_asset_manager_long,
                "percentageOfOpenInterestAssetManagerShort": item.percentage_of_open_interest_asset_manager_short,
                "percentageOfOpenInterestAssetManagerLongShort": item.percentage_of_open_interest_asset_manager_long_short,

                "percentageOfLeverageMoneyAssetManagerLong": item.percentage_of_leverage_money_asset_manager_long,
                "percentageOfLeverageMoneyAssetManagerShort": item.percentage_of_leverage_money_asset_manager_short,
                "percentageOfLeverageMoneyAssetManagerLongShort": item.percentage_of_leverage_money_asset_manager_long_short,

                "percentageOfOtherReptPositionsLongAll": item.percentage_of_other_rept_positions_long_all,
                "percentageOfOtherReptPositionsShortAll": item.percentage_of_other_rept_positions_short_all,
                "percentageOfOtherReptPositionsLongShortAll": item.percentage_of_other_rept_positions_long_short_all,
            })
        
        return Response(response_data)

        # currency_data = {}
        # currency_data['currency'] = {
        #     'name': currency.name,
        #     'verbose_name': currency.verbose_name
        # }

        # # retrieve the latest CurrencyValue object for the given currency
        # latest_currency_value = currency.values.last()

        # if latest_currency_value:
        #     # if there is a latest CurrencyValue object, add its data to the chart data
        #     currency_data['currency']['openPrice'] = latest_currency_value.open_price
        #     currency_data['currency']['closePrice'] = latest_currency_value.close_price
        #     currency_data['currency']['highPrice'] = latest_currency_value.high_price
        #     currency_data['currency']['lowPrice'] = latest_currency_value.low_price
        #     currency_data['currency']['adj_closePrice'] = latest_currency_value.adj_close_price

        # # retrieve the latest CoTFin object for the given currency
        # latest_cotfin = currency.cotfins.last()

        # if latest_cotfin:
        #     # if there is a latest CoTFin object, add its data to the chart data
        #     currency_data['asset_manager_positions_long'] = latest_cotfin.asset_manager_positions_long
        #     currency_data['asset_manager_positions_short'] = latest_cotfin.asset_manager_positions_short
        #     currency_data['asset_manager_positions_long_short'] = latest_cotfin.asset_manager_positions_long_short

        #     currency_data['leverage_money_positions_long'] = latest_cotfin.leverage_money_positions_long
        #     currency_data['leverage_money_positions_short'] = latest_cotfin.leverage_money_positions_short
        #     currency_data['leverage_money_positions_long_short'] = latest_cotfin.leverage_money_positions_long_short

        #     currency_data['other_rept_positions_long_all'] = latest_cotfin.other_rept_positions_long_all
        #     currency_data['other_rept_positions_short_all'] = latest_cotfin.other_rept_positions_short_all
        #     currency_data['other_rept_positions_long_short_all'] = latest_cotfin.other_rept_positions_long_short_all

        #     currency_data['percentage_of_open_interest_asset_manager_long'] = latest_cotfin.percentage_of_open_interest_asset_manager_long
        #     currency_data['percentage_of_open_interest_asset_manager_short'] = latest_cotfin.percentage_of_open_interest_asset_manager_short
        #     currency_data['percentage_of_open_interest_asset_manager_long_short'] = latest_cotfin.percentage_of_open_interest_asset_manager_long_short

        #     currency_data['percentage_of_leverage_money_asset_manager_long'] = latest_cotfin.percentage_of_leverage_money_asset_manager_long
        #     currency_data['percentage_of_leverage_money_asset_manager_short'] = latest_cotfin.percentage_of_leverage_money_asset_manager_short
        #     currency_data['percentage_of_leverage_money_asset_manager_long_short'] = latest_cotfin.percentage_of_leverage_money_asset_manager_long_short

        #     currency_data['percentage_of_other_rept_positions_long_all'] = latest_cotfin.percentage_of_other_rept_positions_long_all
        #     currency_data['percentage_of_other_rept_positions_short_all'] = latest_cotfin.percentage_of_other_rept_positions_short_all
        #     currency_data['percentage_of_other_rept_positions_long_short_all'] = latest_cotfin.percentage_of_other_rept_positions_long_short_all

        # return Response(currency_data)