import json
import pandas as pd
from datetime import datetime, timedelta
import os


def _parse_iso_datetime(iso_str):
    try:
        return datetime.fromisoformat(iso_str)
    except Exception:
        return None


def _duration_str(delta: timedelta):
    hours = delta.seconds // 3600
    minutes = (delta.seconds // 60) % 60
    return f"{hours:02}:{minutes:02}"


def load_and_transform_events(json_path="data/nyc_events_data_all.json") -> pd.DataFrame:
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    records = []

    for event in raw_data:
        try:
            start = _parse_iso_datetime(event["startDate"])
            end = _parse_iso_datetime(event["endDate"])
            if not start or not end:
                continue

            record = {
                "name": event.get("name"),
                "eventCategory": event.get("eventCategory"),
                "eventDate": start.strftime("%Y/%m/%d"),
                "eventTime": start.strftime("%H:%M"),
                "eventWeekday": start.strftime("%A"),
                "eventDateTime": start.strftime("%Y/%m/%d %H:%M"),
                "eventDuration": _duration_str(end - start),
                "startDateISO": event["startDate"],
                "endDateISO": event["endDate"],
                "eventType": event.get("@type"),
                "locationFullAddress": event.get("location", {}).get("address", {}).get("streetAddress"),
                "locationAddressLocality": event.get("location", {}).get("address", {}).get("addressLocality"),
                "locationPostalCode": event.get("location", {}).get("address", {}).get("postalCode"),
                "offerPrices": _format_offers(event.get("offers"))
            }
            records.append(record)
        except Exception:
            continue

    return pd.DataFrame.from_records(records)


def _format_offers(offers):
    if not offers:
        return None

    prices = []
    for offer in offers:
        price = f"{offer.get('price')} {offer.get('priceCurrency')}"
        if "VIP" in offer.get("name", ""):
            prices.append(f"VIP: {price}")
        else:
            prices.append(f"Normal: {price}")
    return ", ".join(prices)


def export_to_excel(df: pd.DataFrame, output_path="output/nyc_events_cleaned.xlsx"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"Data exported to: {output_path}")
