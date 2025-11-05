from typing import List

from django.conf import settings

from indicators.schemas import IndicatorSchema
from indicators.countries import USA


INDICATORS: List[IndicatorSchema] = [
    IndicatorSchema(
        country=USA,
        name="ISM Manufacturing PMI",
        code="ISM",
        url="https://en.macromicro.me/charts/54/ism",
        file=str(settings.BASE_DIR / "indicators/services/usa/ism/data/ISM_historical.json"),
    ),
    IndicatorSchema(
        country=USA,
        name="Non-Manufacturing Indices",
        code="NMI",
        url="https://en.macromicro.me/charts/7/ism",
        file=str(settings.BASE_DIR / "indicators/services/usa/ism/data/nmi_historical.json"),
    ),
]
