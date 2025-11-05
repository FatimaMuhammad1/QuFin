from typing import List
from indicators.schemas import Frequency, IndicatorSchema
from indicators.countries import USA


INDICATORS: List[IndicatorSchema] = [
    IndicatorSchema(
        country=USA,
        name="Producer Price Index by Commodity: All Commodities",
        code="PPIACO",
        url="https://fred.stlouisfed.org/series/PPIACO",
    ),
    IndicatorSchema(
        country=USA,
        name="Producer Price Index by Commodity: Final Demand",
        code="PPIFIS",
        url="https://fred.stlouisfed.org/series/PPIFIS",
    ),
    IndicatorSchema(
        country=USA,
        name="Producer Price Index by Commodity: Final Demand: "\
            "Final Demand Less Foods and Energy",
        code="PPIFES",
        url="https://fred.stlouisfed.org/series/PPIFES",
    ),
    IndicatorSchema(
        country=USA,
        name="Producer Price Index by Commodity: Final Demand: "\
            "Nondurable Consumer Goods Less Foods and Energy",
        code="WPUFD413111",
        url="https://fred.stlouisfed.org/series/WPUFD413111",
    ),
    IndicatorSchema(
        country=USA,
        name="Producer Price Index by Commodity: Final Demand: Finished Goods",
        code="WPSFD49207",
        url="https://fred.stlouisfed.org/series/WPSFD49207",
    ),
    IndicatorSchema(
        country=USA,
        name="Producer Price Index by Commodity: Final Demand: "\
            "Finished Goods Less Foods and Energy (WPSFD4131)",
        code="WPSFD4131",
        url="https://fred.stlouisfed.org/series/WPSFD4131",
    ),
    IndicatorSchema(
        country=USA,
        name="University of Michigan: Consumer Sentiment",
        code="UMCSENT",
        url="https://fred.stlouisfed.org/series/UMCSENT",
    ),
    IndicatorSchema(
        country=USA,
        name="New Privately-Owned Housing Units Authorized in "\
            "Permit-Issuing Places: Total Units",
        code="PERMIT",
        url="https://fred.stlouisfed.org/series/PERMIT",
    ),
    IndicatorSchema(
        country=USA,
        name="New Privately-Owned Housing Units Started: Total Units",
        code="HOUST",
        url="https://fred.stlouisfed.org/series/HOUST",
    ),
    IndicatorSchema(
        country=USA,
        name="M2SL",
        code="M2SL",
        url="https://fred.stlouisfed.org/series/M2SL",
    ),
    IndicatorSchema(
        country=USA,
        name="M2REAL",
        code="M2REAL",
        url="https://fred.stlouisfed.org/series/M2REAL",
    ),
    IndicatorSchema(
        country=USA,
        name="Currency in Circulation",
        code="CURRCIR",
        url="https://fred.stlouisfed.org/series/CURRCIR",
    ),
    IndicatorSchema(
        country=USA,
        name="Velocity of M2 Money Stock",
        code="M2V",
        url="https://fred.stlouisfed.org/series/M2V",
    ),
    IndicatorSchema(
        country=USA,
        name="Effective Federal Funds Rate",
        code="EFFR",
        url="https://fred.stlouisfed.org/series/EFFR",
    ),
    IndicatorSchema(
        country=USA,
        name="Federal Funds Effective Rate",
        code="FEDFUNDS",
        url="https://fred.stlouisfed.org/series/FEDFUNDS",
    ),
    IndicatorSchema(
        country=USA,
        name="Consumer Price Index for All Urban Consumers: "\
            "All Items in U.S. City Average",
        code="CPIAUCSL",
        url="https://fred.stlouisfed.org/series/CPIAUCSL",
    ),
    IndicatorSchema(
        country=USA,
        name="Consumer Price Index for All Urban Consumers: All "\
            "Items Less Food and Energy in U.S. City Average",
        code="CPILFESL",
        url="https://fred.stlouisfed.org/series/CPILFESL",
    ),
    IndicatorSchema(
        country=USA,
        name="All Employees, Total Nonfarm",
        code="PAYEMS",
        url="https://fred.stlouisfed.org/series/PAYEMS",
    ),
    IndicatorSchema(
        country=USA,
        name="Initial Claims",
        code="ICSA",
        url="https://fred.stlouisfed.org/series/ICSA",
        frequency=Frequency.WEEKLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Initial Claims",
        code="ICNSA",
        url="https://fred.stlouisfed.org/series/ICNSA",
        frequency=Frequency.WEEKLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Job Openings: Total Nonfarm",
        code="JTSJOL",
        url="https://fred.stlouisfed.org/series/JTSJOL",
    ),
    IndicatorSchema(
        country=USA,
        name="Hires: Total Nonfarm",
        code="JTSHIL",
        url="https://fred.stlouisfed.org/series/JTSHIL",
    ),
    IndicatorSchema(
        country=USA,
        name="Total Separations: Total Nonfarm",
        code="JTSTSL",
        url="https://fred.stlouisfed.org/series/JTSTSL",
    ),
    IndicatorSchema(
        country=USA,
        name="Advance Retail Sales: Retail Trade and Food Services",
        code="RSAFS",
        url="https://fred.stlouisfed.org/series/RSAFS",
    ),
    IndicatorSchema(
        country=USA,
        name="Advance Real Retail and Food Services Sales",
        code="RRSFS",
        url="https://fred.stlouisfed.org/series/RRSFS",
    ),
    IndicatorSchema(
        country=USA,
        name="Household Debt to GDP for United States",
        code="HDTGPDUSQ163N",
        url="https://fred.stlouisfed.org/series/HDTGPDUSQ163N",
        frequency=Frequency.QUARTERLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Total Credit to Households and Non-Profit Institutions"\
            " Serving Households, Adjusted for Breaks, for United States",
        code="QUSHAM770A",
        url="https://fred.stlouisfed.org/series/QUSHAM770A",
        frequency=Frequency.QUARTERLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Trade Balance: Goods, Balance of Payments Basis",
        code="BOPGTB",
        url="https://fred.stlouisfed.org/series/BOPGTB",
    ),
    IndicatorSchema(
        country=USA,
        name="Trade Balance: Goods and Services, Balance of Payments Basis",
        code="BOPGSTB",
        url="https://fred.stlouisfed.org/series/BOPGSTB",
    ),
    IndicatorSchema(
        country=USA,
        name="Balance of Payments for United States",
        code="USABCAGDPBP6",
        url="https://fred.stlouisfed.org/series/USABCAGDPBP6",
        frequency=Frequency.ANNUAL,
    ),
    IndicatorSchema(
        country=USA,
        name="Balance on current account",
        code="IEABC",
        url="https://fred.stlouisfed.org/series/IEABC",
        frequency=Frequency.QUARTERLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Balance on Current Account, NIPA's",
        code="NETFI",
        url="https://fred.stlouisfed.org/series/NETFI",
        frequency=Frequency.QUARTERLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Balance on capital account",
        code="IEABCP",
        url="https://fred.stlouisfed.org/series/IEABCP",
        frequency=Frequency.QUARTERLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Balance of payments BPM6: Current account Balance: "\
            "Total: Total Balance as % of GDP for the United States",
        code="USAB6BLTT02STSAQ",
        url="https://fred.stlouisfed.org/series/USAB6BLTT02STSAQ",
        frequency=Frequency.QUARTERLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Federal Debt Held by Foreign and International Investors"\
            " as Percent of Gross Domestic Product",
        code="HBFIGDQ188S",
        url="https://fred.stlouisfed.org/series/HBFIGDQ188S",
        frequency=Frequency.QUARTERLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Federal Outlays: Interest as Percent of Gross Domestic Product",
        code="FYOIGDA188S",
        url="https://fred.stlouisfed.org/series/FYOIGDA188S",
        frequency=Frequency.ANNUAL,
    ),
    IndicatorSchema(
        country=USA,
        name="Government current expenditures: Interest payments",
        code="A180RC1Q027SBEA",
        url="https://fred.stlouisfed.org/series/A180RC1Q027SBEA",
        frequency=Frequency.QUARTERLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Federal Debt: Total Public Debt as Percent of Gross Domestic Product",
        code="GFDEGDQ188S",
        url="https://fred.stlouisfed.org/series/GFDEGDQ188S",
        frequency=Frequency.QUARTERLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Market Yield on U.S. Treasury Securities at 10-Year "\
            "Constant Maturity, Quoted on an Investment Basis",
        code="WGS10YR",
        url="https://fred.stlouisfed.org/series/WGS10YR",
        frequency=Frequency.WEEKLY,
    ),
    IndicatorSchema(
        country=USA,
        name="10-Year Treasury Constant Maturity Minus Federal Funds Rate",
        code="T10YFF",
        url="https://fred.stlouisfed.org/series/T10YFF",
        frequency=Frequency.DAILY,
    ),
    IndicatorSchema(
        country=USA,
        name="Moody's Seasoned Baa Corporate Bond Yield Relative "\
            "to Yield on 10-Year Treasury Constant Maturity",
        code="BAA10Y",
        url="https://fred.stlouisfed.org/series/BAA10Y",
        frequency=Frequency.DAILY,
    ),
    IndicatorSchema(
        country=USA,
        name="Moody's Seasoned Baa Corporate Bond Yield Relative "\
            "to Yield on 10-Year Treasury Constant Maturity",
        code="BAA10YM",
        url="https://fred.stlouisfed.org/series/BAA10YM",
    ),
    IndicatorSchema(
        country=USA,
        name="Federal Surplus or Deficit",
        code="FYFSD",
        url="https://fred.stlouisfed.org/series/FYFSD",
        frequency=Frequency.ANNUAL,
    ),
    IndicatorSchema(
        country=USA,
        name="Assets: Total Assets: Total Assets (Less Eliminations"\
            " from Consolidation): Wednesday Level",
        code="WALCL",
        url="https://fred.stlouisfed.org/series/WALCL",
        frequency=Frequency.WEEKLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Assets: Central Bank Liquidity Swaps: Central Bank"\
            " Liquidity Swaps: Wednesday Level",
        code="SWPT",
        url="https://fred.stlouisfed.org/series/SWPT",
        frequency=Frequency.WEEKLY,
    ),
    IndicatorSchema(
        country=USA,
        name="Real Gross Domestic Product",
        code="GDPC1",
        url="https://fred.stlouisfed.org/series/GDPC1",
        frequency=Frequency.QUARTERLY,
    ),
]
