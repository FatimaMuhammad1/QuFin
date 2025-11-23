from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .heatmap.views import fetch_heat_map_data, fetch_country_scores, fetch_country_metrics, fetch_gdp_per_capita_all
from .traders_commitment.views import CurrenciesViewSet, COTDataViewSet
from .indicators.views import CountryViewSet, IndicatorListViewSet, EntriesViewSet


router = SimpleRouter()
router.register("countries", CountryViewSet, basename="countries")
router.register("indicators", IndicatorListViewSet, basename="indicators")
router.register("entries", EntriesViewSet, basename="entries")
router.register("currencies", CurrenciesViewSet, basename="currencies")
router.register("cot", COTDataViewSet, basename="cot")


urlpatterns = [
    path("currency-heatmap/", fetch_heat_map_data),
    path("country-scores/", fetch_country_scores),
    path("country-metrics/<str:iso_code>/", fetch_country_metrics),
    path("gdp-per-capita/", fetch_gdp_per_capita_all),
    path("", include(router.urls)),
]
