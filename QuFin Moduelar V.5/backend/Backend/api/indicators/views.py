from django.utils import timezone

import numpy as np
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from indicators.models import Country, Indicator, Entry
from .serializers import CountrySerializer


class CountryViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Country.objects.all().order_by("name")
    serializer_class = CountrySerializer


class IndicatorListViewSet(GenericViewSet, mixins.ListModelMixin):
    renderer_classes = [JSONRenderer]

    def list(self, request):
        data = self.get_indicator_data()
        return Response(data)

    def get_indicator_data(self):
        indicators = (Indicator.objects.annotate(
            country_codes=Concat(
                "country__code",
                Value(","),
                output_field=CharField()
            )
        )
        .values("code", "name", "country_codes")
        .order_by("code", "name"))

        data = []
        for indicator in indicators:
            country_codes = list(filter(
                lambda value: bool(value),
                indicator["country_codes"].split(",")
            ))
            data.append({
                "code": indicator["code"],
                "name": indicator["name"],
                "countries": country_codes,
            })

        return data


class EntriesViewSet(GenericViewSet, mixins.ListModelMixin):
    renderer_classes = [JSONRenderer]
    LOW_VALUE_THRESHOLD = 100

    def parse_dates(self, request):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if start_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d')
        else:
            start_date = timezone.datetime.min

        if end_date_str:
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d')
        else:
            end_date = timezone.datetime.max
        
        return start_date, end_date
    
    def get_countries_queryset(self, request):
        countries = request.query_params.get('countries', '').split(',')
        if countries:
            queryset = Country.objects.filter(code__in=countries)
        else:
            queryset = Country.objects.all()
        return queryset
    
    def get_indicators_queryset(self, request):
        indicators = request.query_params.get('indicators', '').split(',')
        if indicators:
            queryset = (Indicator.objects.prefetch_related("country")
                                    .filter(code__in=indicators))
        else:
            queryset = Indicator.objects.none()
        return queryset

    def list(self, request):
        data_type = request.query_params.get("data_type", "actual")
        start_date, end_date = self.parse_dates(request)

        countries = self.get_countries_queryset(request)
        indicators = self.get_indicators_queryset(request)

        response_data = []
        for country in countries:
            indicator_data = []

            for indicator in indicators:
                entries = Entry.objects.filter(indicator=indicator, date__gte=start_date,
                                               date__lte=end_date)

                entry_data = []
                values = []
                for entry in entries:
                    entry_data.append({
                        "x": entry.date.isoformat(),
                        "y1":  entry.value1 if data_type == "actual" else entry.perc_change1,
                        "y2":  entry.value2 if data_type == "actual" else entry.perc_change2,
                        "y3":  entry.value3 if data_type == "actual" else entry.perc_change3,
                        "pcy1":  entry.perc_change1,
                        "pcy2":  entry.perc_change2,
                        "pcy3":  entry.perc_change3,
                        "value1_name":  entry.value1_name,
                        "value2_name":  entry.value2_name,
                        "value3_name":  entry.value3_name,
                        "indicatorCode": indicator.code,
                        "countryCode": country.code,
                        "countryName": country.name,
                    })
                    values.extend([entry.value1 if entry.value1 is not None else 0])
                
                if len(values) > 0:
                    mean = sum(values) / len(values)
                    std_dev = np.std(values)
                    z_score = (mean - np.mean(values)) / std_dev
                    if z_score < -1.0:
                        low_value = True
                    else:
                        low_value = False
                else:
                    low_value = None


                indicator_data.append({
                    "name": "{} - {}".format(country.name, indicator.code),
                    "low_value": low_value,
                    "data": entry_data,
                })

            response_data.extend(indicator_data)
        return Response(response_data)
