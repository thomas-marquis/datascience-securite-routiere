import logging

import pandas as pd

from lib.constant import Datasets
from lib.data.accidents.scrappers import get_urls_by_dataset
from lib import utils

urls_map = get_urls_by_dataset()
dtypes_file_path = 'resources/dtypes/raw.yml'

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
def dtypes(data_name: str, base_path: str = '') -> dict:
    assert data_name in Datasets.list_all()

    return utils.get_dtypes(data_name, dtypes_file_path, base_path=base_path)


# load datasets
def get_raw_dataset(data_name: str, base_path: str = '') -> pd.DataFrame:
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
        df: pd.DataFrame = pd.read_csv(url, dtype=dtypes(data_name, base_path=base_path), **read_csv_kwargs)
        logging.info('{} - {} ({}): {} lines'.format(data_name, year, url, df.shape[0]))
        if df_acc is None:
            df_acc = df.copy()
        else:
            df_acc = df_acc.append(df, ignore_index=True)

    return df_acc
