from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .heatmap.views import fetch_heat_map_data, fetch_country_scores
from .traders_commitment.views import CurrenciesViewSet, COTDataViewSet
from .indicators.views import CountryViewSet, IndicatorListViewSet, EntriesViewSet


router = SimpleRouter()
router.register("countries", CountryViewSet, basename="countries")
router.register("indicators", IndicatorListViewSet, basename="indicators")
router.register("entries", EntriesViewSet, basename="entries")
router.register("currencies", CurrenciesViewSet, basename="currencies")
router.register("cot", COTDataViewSet, basename="cot")


urlpatterns = [
    path("api/v1/currency-heatmap/", fetch_heat_map_data),
    path("api/v1/country-scores/", fetch_country_scores),
    path("", include(router.urls)),
]
