from fastapi import APIRouter, HTTPException
import httpx
from typing import Dict

router = APIRouter()

@router.get("/api/v1/country-scores/")
async def fetch_country_scores() -> Dict:
    """Fetch and compute country scores using World Bank indicators."""
    try:
        print("Starting to fetch country scores...")
        
        # World Bank API indicators
        indicators = {
            "gdp_per_capita": "NY.GDP.PCAP.CD",     # GDP per capita (current US$)
            "unemployment": "SL.UEM.TOTL.ZS",        # Unemployment, total (% of labor force)
            "inflation": "FP.CPI.TOTL.ZG",          # Inflation, consumer prices (annual %)
            "exports": "NE.EXP.GNFS.ZS",           # Exports of goods and services (% of GDP)
            "fdi": "BX.KLT.DINV.WD.GD.ZS",        # Foreign direct investment, net inflows (% of GDP)
        }
        
        print("Using indicators:", indicators)
        
        # Use most recent 3 years of data
        current_year = 2023
        years = f"{current_year-3}:{current_year}"
        print(f"Fetching data for years: {years}")
        
        latest = {k: {} for k in indicators.keys()}

        async with httpx.AsyncClient() as client:
            for key, code in indicators.items():
                print(f"Fetching {key} data...")
                url = f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&date={years}&per_page=20000"
                print(f"API URL: {url}")
                try:
                    resp = await client.get(url, timeout=20.0)
                    resp.raise_for_status()
                    j = resp.json()
                    print(f"Received data for {key}: {len(j[1]) if isinstance(j, list) and len(j) > 1 else 0} rows")
                    rows = j[1] if isinstance(j, list) and len(j) > 1 else []
                except Exception as e:
                    print(f"Error fetching {key}: {str(e)}")
                    raise
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

        # Updated weights for comprehensive economic scoring
        weights = {
            "gdp_per_capita": 0.35,    # GDP per capita has highest weight
            "unemployment": 0.25,       # Unemployment is significant
            "inflation": 0.15,          # Inflation impacts stability
            "exports": 0.15,           # Export performance
            "fdi": 0.10                # Foreign investment attractiveness
        }

        print("Computing scores with indicators:", list(indicators.keys()))
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

        print(f"Final scores computed for {len(scores)} countries")
        print("Sample scores:", dict(list(scores.items())[:5]))
        return scores
    except Exception as e:
        print(f"Error in fetch_country_scores: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 