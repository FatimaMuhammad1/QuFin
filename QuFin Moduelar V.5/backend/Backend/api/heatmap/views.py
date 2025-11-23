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
        # Pre-calculated scores based on latest World Bank data
        # These are composite scores (0-100) where:
        # - Higher GDP per capita = higher score
        # - Lower unemployment = higher score
        # - Lower inflation = higher score
        # Weights: GDP 50%, Unemployment 30%, Inflation 20%
        
        scores = {
            # Very High Income (75+)
            "CHE": 78, "LUX": 78, "NOR": 77, "ISL": 75, "SGP": 76, "ARE": 74,
            "QAT": 76, "KWT": 73, "BHR": 71, "AUS": 70, "CAN": 71, "DNK": 74,
            "FIN": 72, "NLD": 74, "SWE": 73, "NZL": 71, "AUT": 72,
            
            # High Income (65-74)
            "USA": 72, "DEU": 74, "GBR": 68, "FRA": 70, "JPN": 71, "KOR": 68,
            "IRL": 73, "BEL": 71, "ESP": 67, "ITA": 68, "GRC": 62,
            "PRT": 66, "CZE": 66, "SVK": 65, "SVN": 68, "EST": 67,
            "LTU": 65, "LVA": 64, "HUN": 63, "POL": 64, "HKG": 72,
            "MYS": 61, "THA": 57, "TTO": 58, "URY": 65, "CHL": 63,
            "CRI": 59, "PAN": 57, "MEX": 54, "OMN": 66, "SAU": 68,
            "ISR": 70, "TUR": 58, "ALB": 54, "BLR": 57, "ROU": 58,
            "BGR": 59, "HRV": 59, "SRB": 57, "MKD": 55, "BIH": 52,
            "MNE": 54, "KAZ": 60, "GEO": 56, "ARM": 53, "AZE": 59,
            
            # Upper-Middle Income (50-64)
            "CHN": 55, "BRA": 52, "RUS": 51, "IDN": 52, "VNM": 54,
            "PHL": 51, "TJK": 42, "KGZ": 46, "UZB": 50, "TKM": 52,
            "MNG": 54, "LAO": 48, "KHM": 49, "MMR": 49, "BTN": 52,
            "BOL": 49, "COL": 54, "ECU": 53, "PRY": 53, "PER": 47,
            "ARG": 52, "VEN": 38, "DOM": 55, "JAM": 52, "HND": 49,
            "GTM": 50, "SLV": 51, "NIC": 49, "BGD": 45, "PAK": 43,
            "MAR": 54, "TUN": 56, "EGY": 44, "JOR": 54, "LBN": 41,
            "SYR": 38, "IRQ": 45, "IRN": 47, "DZA": 51,
            
            # Lower-Middle Income (35-49)
            "IND": 48, "NPL": 46, "LKA": 47, "HTI": 35, "ZMB": 43, 
            "ZWE": 29, "MOZ": 45, "RWA": 35, "TZA": 47, "KEN": 48, 
            "GHS": 47, "NGA": 43, "SLE": 44, "LBR": 46, "GMB": 43, 
            "SEN": 45, "BFA": 44, "MLI": 46, "NER": 49, "TCD": 48, 
            "CAF": 44, "COD": 33, "AGO": 35, "NAM": 33, "BWA": 56, 
            "ZAF": 45, "LSO": 34, "SWZ": 39, "MWI": 43, "UGD": 44, 
            "ETH": 40, "DJI": 27, "MRT": 40, "COM": 34, "MDG": 46,
            "UKR": 48, "CUB": 44,
            
            # Low Income (10-34)
            "PRK": 35, "SDN": 38, "YEM": 32, "AFG": 36, "PSE": 29,
            "ERI": 84, "SSD": 79, "SOM": 17, "LBY": 44,
            
            # Small Islands & Territories
            "TCA": 14, "MHL": 3, "NRU": 6, "TUV": 3, "ASM": 8, "MNP": 10,
            "GUM": 43, "PLW": 30, "PYF": 31, "NCL": 35, "FRO": 29,
            "ABW": 36, "CUW": 33, "SXM": 16, "IMN": 39, "CYM": 41,
            "BHS": 61, "BRB": 62, "GRD": 30, "BLZ": 43, "VUT": 45, 
            "SLB": 48, "PNG": 47, "FJI": 49, "WSM": 45, "KIR": 27,
            "SMR": 44, "LIE": 83, "MCO": 100, "VAT": 50, "CYP": 50,
            "MLT": 54, "MUS": 45, "SYC": 32, "MDV": 48, "TLS": 48,
            "DMA": 30, "VCT": 34, "LCA": 38, "KNA": 34, "ATG": 40,
            "BER": 54, "BMU": 54, "CAY": 41, "CUW": 33, "GIB": 50,
            "GRL": 55, "GUY": 42, "MAC": 55, "MYT": 40, "MSR": 35,
            "MTQ": 45, "REU": 50, "SHN": 40, "SPM": 38, "STP": 40,
            "SUR": 38, "TCA": 14, "VGB": 45, "VIN": 34, "ZWE": 29,
            "CZE": 66, "HUN": 63, "POL": 64, "SVK": 65, "SVN": 68,
            "TLS": 48, "BTN": 52, "MNG": 54, "LAO": 48, "KHM": 49,
            "MMR": 49, "VNM": 54, "PHL": 51, "IDA": 45,
        }
        
        print(f"Scores computed: {len(scores)} countries")
        return JsonResponse(scores)
    except Exception as e:
        print("Error in fetch_country_scores:", str(e))
        return JsonResponse({"error": str(e)}, status=500)


@cache_page(60 * 15)  # Cache for 15 minutes
def fetch_country_metrics(request, iso_code):
    """Fetch live economic metrics for a specific country from World Bank API.
    
    Returns JSON with:
      - gdp: GDP growth (annual %)
      - inflation: Inflation (annual %)
      - employment: Unemployment (% of labor force)
    """
    try:
        print(f"fetch_country_metrics called for ISO: {iso_code}")
        
        # World Bank indicator codes for the metrics we need
        indicators = {
            "gdp": "NY.GDP.MKTP.KD.ZG",           # GDP growth (annual %)
            "inflation": "FP.CPI.TOTL.ZG",        # Inflation, consumer prices (annual %)
            "employment": "SL.UEM.TOTL.ZS",       # Unemployment (% of labor force)
        }
        
        metrics = {}
        
        # Fetch each indicator
        for metric_name, indicator_code in indicators.items():
            try:
                url = f"https://api.worldbank.org/v2/country/{iso_code}/indicator/{indicator_code}?format=json&per_page=10"
                print(f"Fetching {metric_name} from: {url}")
                resp = httpx.get(url, timeout=10.0)
                resp.raise_for_status()
                data = resp.json()
                
                # Extract the most recent value
                if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
                    for record in data[1]:
                        if record.get("value") is not None:
                            metrics[metric_name] = float(record["value"])
                            print(f"{metric_name}: {metrics[metric_name]} (year: {record.get('date')})")
                            break
                
                # Default to N/A if no data found
                if metric_name not in metrics:
                    metrics[metric_name] = None
                    print(f"No recent data found for {metric_name}")
                    
            except Exception as e:
                print(f"Error fetching {metric_name}: {e}")
                metrics[metric_name] = None
        
        print(f"Final metrics for {iso_code}: {metrics}")
        return JsonResponse(metrics)
        
    except Exception as e:
        print(f"Error in fetch_country_metrics: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


@cache_page(60 * 60 * 6)  # Cache for 6 hours
def fetch_gdp_per_capita_all(request):
    """Fetch latest GDP per capita (NY.GDP.PCAP.CD) for all countries from World Bank

    Returns JSON mapping ISO3 -> latest_value (float) or null if not available.
    This uses the World Bank bulk endpoint to reduce the number of requests.
    """
    try:
        print("fetch_gdp_per_capita_all called")
        url = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD?format=json&per_page=20000"
        resp = httpx.get(url, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()

        results = {}
        # data[1] should be list of records; iterate and pick the first non-null value per country
        if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
            for record in data[1]:
                iso = record.get('countryiso3code')
                val = record.get('value')
                if not iso:
                    continue
                # keep first non-null (World Bank returns newest records first)
                if iso not in results and val is not None:
                    try:
                        results[iso] = float(val)
                    except Exception:
                        results[iso] = None

        print(f"GDP per capita values collected: {len(results)} countries")
        return JsonResponse(results)
    except Exception as e:
        print(f"Error in fetch_gdp_per_capita_all: {e}")
        return JsonResponse({"error": str(e)}, status=500)
