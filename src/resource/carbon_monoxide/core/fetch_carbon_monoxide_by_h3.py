from src.resource.carbon_monoxide.core.fetch_carbon_monoxide import get_date, \
    fetch_carbon_monoxide_data, get_h3_indexes
import pandas as pd


def get_carbon_monoxide_details_by_h3(request_body):
    rolling = request_body.rolling
    air_quality = fetch_carbon_monoxide_data()
    air_quality = settings.emission_data
    if not settings.emission_data:
        start_day, end_day = get_date(interval=30)
        air_quality = fetch_carbon_monoxide_data(start_day, end_day)
        settings.emission_data = air_quality.to_json()
    h3_indexes = get_h3_indexes(gpd.GeoDataFrame.from_features(json.loads(air_quality))if type(air_quality) == str else air_quality)
    hdf = h3_indexes[h3_indexes['h3'] == request_body.h3_index]
    hdf_davg = hdf.groupby(pd.Grouper(freq='D', key='timestamp')).mean()
    hdf_davg.index= hdf_davg.index.date
    hdf_avg = hdf_davg.fillna(method='ffill')
    hdf_avg[f'd{rolling}_rolling']=hdf_avg['value'].rolling(rolling).mean()
    hdf_avg = hdf_avg.fillna("")

    return hdf_avg.to_dict("records")
