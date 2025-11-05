# from datetime import date, datetime
# import asyncio
# import httpx
# from enum import Enum
# from typing import List, Dict, Union
# import io
# import csv

# from pydantic import BaseModel


# class Frequency(Enum):
#     DAILY = 1
#     WEEKLY = 2
#     MONTHLY = 3
#     QUARTERLY = 4
#     ANNUAL = 5


# class CountrySchema(BaseModel):
#     code: str
#     name: str


# class EntrySchema(BaseModel):
#     country: CountrySchema
#     name: str
#     code: str
#     date: date
#     value1_name: str | None = None
#     value1: float | None
#     value2_name: str | None = None
#     value2: float | None = None
#     value3_name: str | None = None
#     value3: float | None = None
#     total_value: float | None = None
#     perc_change1: float
#     perc_change2: float | None = None
#     perc_change3: float | None = None
#     frequency: Frequency = Frequency.MONTHLY
#     unit: str | None = None


# class IndicatorSchema(BaseModel):
#     country: CountrySchema
#     name: str
#     code: str
#     url: str | None
#     frequency: Frequency = Frequency.MONTHLY
#     file: str | None = None
#     unit: str | None = None

#     def __hash__(self) -> int:
#         return int("".join([str(ord(char)) for char in self.code]))


# AUS = CountrySchema(code="AUS	", name="Australia")


# _BASE_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"


# def get_indicators() -> List[IndicatorSchema]:
#     return [
#         IndicatorSchema(
#             country=AUS,
#             name="Business Tendency Surveys for Manufacturing: (Confidence Indicators)",
#             code="BSCICP02AUQ460S",
#             url="https://fred.stlouisfed.org/series/BSCICP02AUQ460S",
#         ),
#         IndicatorSchema(
#             country=AUS,
#             name="Leading Indicator for Production: (BTC OECD Series)",
#             code="LOCOBPORAUQ460S",
#             url="https://fred.stlouisfed.org/series/LOCOBPORAUQ460S",
#             frequency=Frequency.QUARTERLY,
#         ),
#         IndicatorSchema(
#             country=AUS,
#             name="PPI Total Manufacturing (2015=100 Index)",
#             code="PIEAMP01AUQ661N",
#             url="https://fred.stlouisfed.org/series/PIEAMP01AUQ661N",
#             frequency=Frequency.QUARTERLY,
#         ),
#         IndicatorSchema(
#             country=AUS,
#             name="PPI: Final Demand Services (2009=100 index)",
#             code="PPIDSS",
#             url="https://fred.stlouisfed.org/series/PPIDSS",
#         ),
#         IndicatorSchema(
#             country=AUS,
#             name="PPI: Manufacture of Food Products (2015=100 Index)",
#             code="PIEAFD01AUQ661N",
#             url="https://fred.stlouisfed.org/series/PIEAFD01AUQ661N",
#             frequency=Frequency.QUARTERLY,
#         ),
#         IndicatorSchema(
#             country=AUS,
#             name="PPI: Finished Goods (2015=100 Index)",
#             code="PISPFG01AUQ661N",
#             url="https://fred.stlouisfed.org/series/PISPFG01AUQ661N",
#         ),
#         IndicatorSchema(
#             country=AUS,
#             name="Industrial Production Growth Rate (Excluding Construction)",
#             code="PRINTO01AUQ657S",
#             url="https://fred.stlouisfed.org/series/PRINTO01AUQ657S",
#             frequency=Frequency.QUARTERLY,
#         ),
#         IndicatorSchema(
#             country=AUS,
#             name="Consumer Sentiment | Confidence (Percentage)",
#             code="CSCICP02AUM460S",
#             url="https://fred.stlouisfed.org/series/CSCICP02AUM460S",
#         ),
#     ]


# async def _async_get_all_data(
#     indicators: List[IndicatorSchema],
#     start_date: str = "1950-01-01",
#     end_date: str = str(datetime.now().date()),
# ) -> Dict[IndicatorSchema, httpx.Response]:
#     results: List[httpx.Response] = []

#     async with httpx.AsyncClient(timeout=30.0) as client:
#         tasks = [
#             client.get(
#                 _BASE_URL,
#                 params={"id": indicator.code, "cosd": start_date, "coed": end_date},
#             )
#             for indicator in indicators
#         ]
#         results = await asyncio.gather(*tasks)

#     responses: Dict[IndicatorSchema, httpx.Response] = dict()

#     for indicator, result in zip(indicators, results):
#         responses[indicator] = result

#     return responses


# def _collect_responses(
#     indicators: List[IndicatorSchema],
# ) -> Dict[IndicatorSchema, httpx.Response]:
#     loop = asyncio.get_event_loop()
#     results: Dict[IndicatorSchema, httpx.Response] = loop.run_until_complete(
#         _async_get_all_data(indicators=indicators)
#     )
#     return results


# def _extract_output_data(
#     responses: Dict[IndicatorSchema, httpx.Response]
# ) -> List[EntrySchema]:
#     entries: List[EntrySchema] = []

#     for indicator, response in responses.items():
#         prev_value: Union[float, None] = None
#         current_value: Union[float, None] = None

#         with open(f"{indicator.code}.csv", "w") as file:
#             file.write(response.text)

#         for item in list(csv.DictReader(io.StringIO(response.text))):
#             try:
#                 current_value = float(item[indicator.code])
#             except Exception:
#                 current_value = None

#             if current_value is not None and prev_value not in [None, 0.0]:
#                 perc_change = round(
#                     (current_value - prev_value) / prev_value, ndigits=6  # type: ignore
#                 )
#             else:
#                 perc_change = 0.0

#             try:
#                 item["DATE"]
#             except:
#                 print(item)
#                 print(indicator.url)
#                 print("------------------")

#             entry = EntrySchema(
#                 country=AUS,
#                 name=indicator.name,
#                 code=indicator.code,
#                 date=datetime.strptime(item["DATE"], "%Y-%m-%d").date(),
#                 value1=current_value,
#                 perc_change1=perc_change,
#             )
#             entries.append(entry)

#             prev_value = current_value

#     return entries


# def get_entries() -> List[EntrySchema]:
#     responses: Dict[IndicatorSchema, httpx.Response] = _collect_responses(
#         indicators=get_indicators()
#     )
#     output_data: List[EntrySchema] = _extract_output_data(responses=responses)
#     return output_data


# get_entries()
