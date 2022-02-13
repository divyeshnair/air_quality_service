from src.resource.carbon_monoxide.core.fetch_carbon_monoxide import get_date, \
    fetch_carbon_monoxide_data, get_h3_indexes
import pandas as pd


def get_carbon_monoxide_details_by_h3(request_body):
    start_day, end_day = get_date(interval=30)
    rolling = request_body.rolling
    air_quality = fetch_carbon_monoxide_data(start_day, end_day)
    h3_indexes = get_h3_indexes(air_quality)
    hdf = h3_indexes[h3_indexes['h3'] == request_body.h3_index]
    hdf_davg = hdf.groupby(pd.Grouper(freq='D', key='timestamp')).mean()
    hdf_davg.index= hdf_davg.index.date
    hdf_avg = hdf_davg.fillna(method='ffill')
    hdf_avg[f'd{rolling}_rolling']=hdf_avg['value'].rolling(rolling).mean()
    hdf_avg = hdf_avg.fillna("")

    return hdf_avg.to_dict("records")
