import json

import geopandas as gpd
from datetime import date, datetime, timedelta
from h3 import h3
import pandas as pd
from extensions import settings


def fetch_carbon_monoxide_data(start_day, end_day):
    query_string = f"carbonmonoxide/geo.json?country=USA&begin={start_day}&end=" \
                   f"{end_day}&limit={settings.record_limit}&offset=0"
    url = settings.emissions_url + query_string
    air_quality = gpd.read_file(url)
    return air_quality


def get_date(start_date=None, end_date=None, interval=None):
    if start_date and end_date:
        start_date_time = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_time = datetime.strptime(end_date, '%Y-%m-%d')
        return start_date_time.strftime("%Y-%m-%d"), end_date_time.strftime(
            "%Y-%m-%d")

    start_day = date.today() - timedelta(days=30)
    today = date.today()
    return start_day.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


def lat_lng_to_h3(row, h3_level=3):
    return h3.geo_to_h3(row.lat, row.lng, h3_level)


def get_h3_indexes(air_quality):
    air_quality['timestamp'] = pd.to_datetime(air_quality['timestamp'])
    air_quality['lng'] = air_quality.geometry.x
    air_quality['lat'] = air_quality.geometry.y
    air_quality = air_quality.drop(['geometry'], axis=1)
    air_quality['h3'] = air_quality.apply(lat_lng_to_h3, axis=1)
    air_quality.set_index(['timestamp'])
    return air_quality


def get_h3_details(request_body):
    air_quality = settings.emission_data
    if not settings.emission_data:
        start_day, end_day = get_date(request_body.start_date, request_body.end_date)
        air_quality = fetch_carbon_monoxide_data(start_day, end_day)
        settings.emission_data = air_quality.to_json()
    h3_indexes = get_h3_indexes(gpd.GeoDataFrame.from_features(json.loads(air_quality))if type(air_quality) == str else air_quality)
    return h3_indexes[["timestamp", "h3"]].to_dict("records")
