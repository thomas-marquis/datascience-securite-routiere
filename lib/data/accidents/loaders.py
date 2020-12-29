import logging

import pandas as pd

from lib.data.accidents.scrappers import get_urls_by_dataset
from lib.constant import Datasets

urls_map = get_urls_by_dataset()

read_csv_kwargs_by_year = {
    'default': {
        'sep': ',',
        'header': 0,
        'encoding': 'latin_1',
    },
    2019: {
        'sep': ';',
        'header': 0,
    },
}


# dtypes
def dtypes(data_name: str) -> dict:
    if data_name == Datasets.CARACS:
        return {
            'Num_Acc': 'string',
            'jour': 'Int32',
            'mois': 'Int32',
            'an': 'string',
            'hrmn': 'string',
            'lum': 'category',
            'dep': 'category',
            'com': 'string',
            'agg': 'category',
            'int': 'category',
            'atm': 'category',
            'col': 'category',
            'gps': 'category',
            'adr': 'string',
            'lat': 'string',
            'long': 'string',
        }
    elif data_name == Datasets.LOCATIONS:
        return {
            'Num_Acc': 'string',
            'catr': 'category',
            'voie': 'string',
            'v1': 'string',
            'v2': 'string',
            'circ': 'category',
            'nbv': 'Int32',
            'vosp': 'category',
            'prof': 'category',
            'pr': 'string',
            'pr1': 'string',
            'plan': 'category',
            'lartpc': 'string',
            'larrout': 'string',
            'surf': 'category',
            'infra': 'category',
            'situ': 'category',
            'env1': 'Int32',
        }
    elif data_name == Datasets.VEHICLES:
        return {
            'Num_Acc': 'string',
            'id_vehicule': 'string',
            'num_veh': 'string',
            'senc': 'category',
            'catv': 'category',
            'obs': 'category',
            'obsm': 'category',
            'choc': 'category',
            'manv': 'category',
            'motor': 'category',
            'occutc': 'Int32',
        }
    elif data_name == Datasets.USERS:
        return {
            'Num_Acc': 'string',
            'id_vehicule': 'string',
            'num_veh': 'string',
            'place': 'category',
            'catu': 'category',
            'grav': 'category',
            'sexe': 'category',
            'an_nais': 'Int32',
            'trajet': 'category',
            'secu1': 'category',
            'secu2': 'category',
            'secu3': 'category',
            'locp': 'category',
            'actp': 'category',
            'etatp': 'category',
            'secu': 'category',
        }
    else:
        raise ValueError(data_name)


# load datasets
def get_raw_dataset(data_name: str) -> pd.DataFrame:
    assert data_name in Datasets.list_all()
    urls_by_year: dict = urls_map[data_name]

    df_acc = None
    for year in urls_by_year:
        url = urls_by_year[year]

        # get read_csv kwargs
        read_csv_kwargs = read_csv_kwargs_by_year['default']
        for kwargs_year in read_csv_kwargs_by_year:
            if year == kwargs_year:
                read_csv_kwargs = read_csv_kwargs_by_year[kwargs_year]

        # get and concat dataframe
        df: pd.DataFrame = pd.read_csv(url, dtype=dtypes(data_name), **read_csv_kwargs)
        logging.info('{} - {} ({}): {} lines'.format(data_name, year, url, df.shape[0]))
        if df_acc is None:
            df_acc = df.copy()
        else:
            df_acc = df_acc.append(df, ignore_index=True)

    return df_acc
