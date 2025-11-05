from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from heatmap.models import ExchangeRate
import httpx


@cache_page(60 * 5)  # Cache for 5 minutes
def fetch_heat_map_data(request, time_frame):
    # Calculate date range based on time frame
    today = datetime.now().date()
    if time_frame == "hourly":
        start_date = datetime.now() - timedelta(hours=1)
    elif time_frame == "4-hours":
        start_date = datetime.now() - timedelta(hours=4)
    elif time_frame == "daily":
        start_date = today - timedelta(days=1)
    elif time_frame == "weekly":
        start_date = today - timedelta(days=7)
    elif time_frame == "monthly":
        start_date = today - timedelta(days=30)
    else:
        return JsonResponse({"error": "Invalid time frame"}, status=400)

    # Retrieve exchange rates from database
    exchange_rates = ExchangeRate.objects.filter(created_at__gte=start_date, created_at__lt=today).values(
        "currency_code", "target_currency_code", "value"
    )

    # Calculate percentage changes
    heat_map_data = {}
    for exchange_rate in exchange_rates:
        currency_code = exchange_rate["currency_code"]
        target_currency_code = exchange_rate["target_currency_code"]
        value = exchange_rate["value"]
        previous_value = (
            ExchangeRate.objects.filter(
                currency_code=currency_code,
                target_currency_code=target_currency_code,
                created_at__lt=start_date,
            )
            .order_by("-created_at")
            .values_list("value", flat=True)
            .first()
        )
        if previous_value is None:
            percentage_change = 0
        else:
            percentage_change = (value - previous_value) / previous_value * 100
        if currency_code not in heat_map_data:
            heat_map_data[currency_code] = {}
        heat_map_data[currency_code][target_currency_code] = {
            "value": value,
            "percentageChange": percentage_change,
        }

    return JsonResponse(heat_map_data)


@cache_page(60 * 15)  # Cache for 15 minutes
def fetch_country_scores(request):
    """Server-side composite country score using World Bank indicators.

    Returns JSON mapping ISO3 -> score (0-100). Uses three indicators:
      - NY.GDP.PCAP.CD (GDP per capita)  -- higher is better
      - SL.UEM.TOTL.ZS (Unemployment %)  -- higher is worse (inverted)
      - FP.CPI.TOTL.ZG (Inflation %)     -- higher is worse (inverted)

    Weights: GDP 0.5, Unemployment 0.3, Inflation 0.2. Missing values are ignored and weights rescaled.
    """
    print("fetch_country_scores endpoint called")
    try:
        indicators = {
            "gdp_per_capita": "NY.GDP.PCAP.CD",
            "unemployment": "SL.UEM.TOTL.ZS",
            "inflation": "FP.CPI.TOTL.ZG",
        }
        years = "2019:2022"

        latest = {k: {} for k in indicators.keys()}

        for key, code in indicators.items():
            url = f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&date={years}&per_page=20000"
            print(f"Fetching data for {key} from {url}")
            resp = httpx.get(url, timeout=20.0)
            resp.raise_for_status()
            j = resp.json()
            rows = j[1] if isinstance(j, list) and len(j) > 1 else []
            for row in rows:
                iso3 = row.get("countryiso3code")
                if not iso3:
                    continue
                val = row.get("value")
                if val is None:
                    continue
                try:
                    year = int(row.get("date", 0))
                except Exception:
                    year = 0
                if iso3 not in latest[key] or year > latest[key][iso3]["year"]:
                    latest[key][iso3] = {"value": float(val), "year": year}

        # collect ISO3 set
        iso_set = set()
        for k in latest:
            iso_set.update(latest[k].keys())

        # compute ranges per indicator
        ranges = {}
        for k in latest:
            arr = [v["value"] for v in latest[k].values()]
            if arr:
                ranges[k] = {"min": min(arr), "max": max(arr)}
            else:
                ranges[k] = None

        weights = {"gdp_per_capita": 0.5, "unemployment": 0.3, "inflation": 0.2}

        scores = {}
        for iso in iso_set:
            total = 0.0
            weight_sum = 0.0
            for k in indicators.keys():
                obj = latest.get(k, {}).get(iso)
                if not obj or ranges.get(k) is None:
                    continue
                v = obj["value"]
                r = ranges[k]
                if r["max"] > r["min"]:
                    norm = ((v - r["min"]) / (r["max"] - r["min"])) * 100.0
                else:
                    norm = 50.0
                # invert unemployment and inflation (higher is worse)
                if k in ("unemployment", "inflation"):
                    norm = 100.0 - norm
                w = weights.get(k, 0.0)
                total += norm * w
                weight_sum += w
            if weight_sum > 0:
                scores[iso] = int(round(total / weight_sum))

        print("Scores computed:", scores)
        return JsonResponse(scores)
    except Exception as e:
        print("Error in fetch_country_scores:", str(e))
        return JsonResponse({"error": str(e)}, status=500)


# 1 2 3 4 5 6 7 8 9 10
