import io
import zipfile
import logging
from pathlib import Path
from datetime import datetime, date

import httpx
import pandas as pd
import numpy as np
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from traders_commitment.models import CoTFORScrapedStatus, Currency, CoTFin
from traders_commitment.schemas import CurrencyData, CoTFinData
from traders_commitment.constants import CURRENCIES



logger = logging.getLogger(__name__)


def _check_cot_history() -> dict[date, bool]:
    logger.info("Checking COT history...")

    output: dict[date, bool] = {}
    for year in range(2006, datetime.now().year):
        output[date(year, 1, 1)] = CoTFORScrapedStatus.objects.filter(
            date__year=year
        ).exists()

    logger.info("COT scrapers status history")
    logger.info(str(output))

    return output


def _get_cot_download_links() -> dict[date, str|Path]:
    years_status: dict[date, bool] = _check_cot_history()
    links: dict[date, str|Path] = {}

    HISTORY_FILE: Path = Path("traders_commitment/services/data/CoT_2006_2022.xlsx")

    for date_item, status in years_status.items():
        if status is True:
            continue

        if 2006 <= date_item.year <= 2022 and HISTORY_FILE not in links.values():
            links[date_item] = HISTORY_FILE

        elif date_item.year > 2022:
            links[date_item] = "https://www.cftc.gov/files/dea/history/"\
                              f"fut_fin_xls_{date_item.year}.zip"
    
    this_year = date(datetime.now().year, 1, 1)
    links[this_year] = f"https://www.cftc.gov/files/dea/history/fut_fin_xls_{this_year.year}.zip"

    return links


def _download_cot_files(links: dict[date, str|Path]) -> dict[date, CoTFORScrapedStatus]:
    paths: dict[date, CoTFORScrapedStatus] = {}

    for date_key in links:
        paths[date_key] = _download_cot_file(date_key, links[date_key])

    return paths


def _download_cot_file(date_key: date, url: str|Path) -> CoTFORScrapedStatus:
    # Check if the file has already been downloaded
    try:
        scraped_status = CoTFORScrapedStatus.objects.get(url=url)
        if scraped_status.file:
            # If the file has already been downloaded, return its path
            logger.info(f"File {scraped_status.file.name} already exists. Skipping download.")
            return scraped_status
    except CoTFORScrapedStatus.DoesNotExist:
        pass

    if isinstance(url, str):
        # Download and extract the file
        filename = url.split("/")[-1].replace(".zip", ".csv")
        response = httpx.get(url, follow_redirects=True, timeout=30)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
            file_content = zip_ref.read(zip_ref.namelist()[0])

        # Save the extracted content to a new file
        extracted_file_path = Path(settings.MEDIA_ROOT, "cotfor", filename)
        with open(extracted_file_path, 'wb') as extracted_file:
            extracted_file.write(file_content)

    elif isinstance(url, Path):
        filename = url.name
        with open(url, "rb") as file:
            file_content = file.read()

    # Update the scraped status with the new file and date
    scraped_status = CoTFORScrapedStatus(url=url, date=date_key)
    scraped_status.file.save(filename, ContentFile(file_content))
    scraped_status.save()

    logger.info(f"File {filename} downloaded and extracted successfully.")

    return scraped_status


def convert_to_int(value) -> int:
    if isinstance(value, int):
        return value
    elif np.isnan(value):
        return 0
    elif isinstance(value, float):
        return int(value)
    else:
        logger.error("Converting this type to float is "\
                     f"not implemented. Type: {str(type(value))} | value: {value}")

        raise Exception("Converting this type to float is "\
                        f"not implemented. Type: {str(type(value))}")


def _read_cot_data(file: CoTFORScrapedStatus) -> list[CoTFinData]:
    df = pd.read_excel(file.file.path)

    output: list[CoTFinData] = []
    currencies: dict[str, CurrencyData] = {}

    for index, row in df.iterrows():
        verbose_name: str = str(row["Market_and_Exchange_Names"]).strip()
        if verbose_name in currencies:
            currency = currencies[verbose_name]
        else:
            for currency in CURRENCIES:
                if currency.verbose_name.strip() == verbose_name:
                    currencies[verbose_name] = currency
                    break
            else:
                currency = None
        
        if currency is None:
            continue

        cot = CoTFinData(
            currency=currency,
            date=datetime.strptime(str(row["Report_Date_as_MM_DD_YYYY"]),
                                "%Y-%m-%d %H:%M:%S").date(),

            
            asset_manager_positions_long=convert_to_int(row["Asset_Mgr_Positions_Long_All"]),
            asset_manager_positions_short=convert_to_int(row["Asset_Mgr_Positions_Short_All"]),
            asset_manager_positions_long_short=(
                convert_to_int(row["Asset_Mgr_Positions_Long_All"]) -
                convert_to_int(row["Asset_Mgr_Positions_Short_All"])
            ),

            leverage_money_positions_long=convert_to_int(row["Lev_Money_Positions_Long_All"]),
            leverage_money_positions_short=convert_to_int(row["Lev_Money_Positions_Short_All"]),
            leverage_money_positions_long_short=(
                convert_to_int(row["Lev_Money_Positions_Long_All"]) -
                convert_to_int(row["Lev_Money_Positions_Short_All"])
            ),

            other_rept_positions_long_all=convert_to_int(row["Other_Rept_Positions_Long_All"]),
            other_rept_positions_short_all=convert_to_int(row["Other_Rept_Positions_Short_All"]),
            other_rept_positions_long_short_all=(
                convert_to_int(row["Other_Rept_Positions_Long_All"]) -
                convert_to_int(row["Other_Rept_Positions_Short_All"])
            ),

            percentage_of_open_interest_asset_manager_long=convert_to_int(row["Pct_of_OI_Asset_Mgr_Long_All"]),
            percentage_of_open_interest_asset_manager_short=convert_to_int(row["Pct_of_OI_Asset_Mgr_Short_All"]),
            percentage_of_open_interest_asset_manager_long_short=(
                convert_to_int(row["Pct_of_OI_Asset_Mgr_Long_All"]) -
                convert_to_int(row["Pct_of_OI_Asset_Mgr_Short_All"])
            ),

            percentage_of_leverage_money_asset_manager_long=convert_to_int(row["Pct_of_OI_Lev_Money_Long_All"]),
            percentage_of_leverage_money_asset_manager_short=convert_to_int(row["Pct_of_OI_Lev_Money_Short_All"]),
            percentage_of_leverage_money_asset_manager_long_short=(
                convert_to_int(row["Pct_of_OI_Lev_Money_Long_All"]) -
                convert_to_int(row["Pct_of_OI_Lev_Money_Short_All"])
            ),

            percentage_of_other_rept_positions_long_all=convert_to_int(row["Pct_of_OI_Other_Rept_Long_All"]),
            percentage_of_other_rept_positions_short_all=convert_to_int(row["Pct_of_OI_Other_Rept_Long_All"]),
            percentage_of_other_rept_positions_long_short_all=(
                convert_to_int(row["Pct_of_OI_Other_Rept_Long_All"]) -
                convert_to_int(row["Pct_of_OI_Other_Rept_Long_All"])
            )
        )
        output.append(cot)
    
    logger.info("Finished reading data from CoT files!")

    return output


def parse_cot_data() -> dict[CoTFORScrapedStatus, list[CoTFinData]]:
    download_links: dict[date, str|Path] = _get_cot_download_links()
    keys = list(download_links.keys())
    keys.sort()

    files: dict[date, CoTFORScrapedStatus] = _download_cot_files(links=download_links)

    output: dict[CoTFORScrapedStatus, list[CoTFinData]] = {}

    for date_key in files:
        file = files[date_key]
        if not file.is_parsed:
            output[file] = _read_cot_data(file)

    return output


def populate_db_with_cot(data: dict[CoTFORScrapedStatus, list[CoTFinData]]):
    currencies: dict[str, Currency] = {}

    logger.info("Starting to populate db with COT data...")

    with transaction.atomic():
        try:
            for status, values in data.items():
                for item in values:
                    if item.currency.name in currencies:
                        currency = currencies[item.currency.name]
                    else:
                        currency, _ = Currency.objects.get_or_create(
                            name=item.currency.name,
                            verbose_name=item.currency.verbose_name
                        )
                        currencies[item.currency.name] = currency

                    cot_data: dict = {**item.dict(), "currency": currency}
                    cot_model = CoTFin.objects.filter(**cot_data).first()

                    if cot_model is None:
                        cot_model = CoTFin(**cot_data)
                        cot_model.save()
                
                status.is_parsed = True
                status.save()

                logger.info(f"Finished parsing CoT data from {status.file.path}")
        except Exception as e:
            logger.error(f"Error occured: {str(e)}")
            logger.error("Rollbacking the db...")
            transaction.rollback()

