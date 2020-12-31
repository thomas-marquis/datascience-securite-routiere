import logging
import os

import pandas as pd
import yaml


def get_dataset(file_path: str, dtypes: dict = None, sep: str = ';', **kwargs) -> pd.DataFrame:
    """Load DataFrame from specified path.

    :param str file_path: data file path. e.g. data/interim/mydata.csv
    :param dict dtypes: pandas dtypes dict (optional)
    :param str sep: pd.read_csv separator (default ';')
    :param kwargs: pd.read_csv kwargs
    :return: loaded dataframe
    """

    df = pd.read_csv(file_path, sep=sep, header=0, encoding='utf8', **kwargs)
    if dtypes:
        df = df.astype(dtypes)

    mem_usg = df.memory_usage().sum() / 1024 ** 2
    logging.info('{}: {} lines loaded ({:.2f})Mb'.format(
        file_path, df.shape[0], mem_usg))

    return df


def count_na(df: pd.DataFrame) -> pd.DataFrame:
    """count na per columns in specified DataFrame.

    :param pd.DataFrame df:
    :return: index=df columns, columns=`['na_count', 'na_rate', 'filled_count', 'filled_rate']`
    """

    nas = []
    for col in df.columns:
        na_count = df[col].isna().sum()
        filled_count = df.shape[0] - na_count
        na_rate = na_count / df.shape[0]
        filled_rate = 1 - na_rate
        nas.append({'na_count': na_count,
                    'na_rate': na_rate,
                    'filled_count': filled_count,
                    'filled_rate': filled_rate, })

        logging.debug('{}: {:.2f}% NA'.format(col, na_rate * 100))

    return pd.DataFrame(nas, index=df.columns).sort_values('filled_rate')


def is_file_exists_locally(file_path: str) -> bool:
    """Test local file exists.

    :param str file_path: local relative or absolute file path.
    :returns: True if file exists
    """

    if os.path.exists(file_path):
        logging.info('file {} already exists'.format(file_path))
        return True
    return False


def get_dtypes(data_name: str, dtypes_file_path: str, base_path: str = '') -> dict:
    path = '{}{}'.format(base_path, dtypes_file_path)

    with open(path, 'r') as yml_file:
        types: dict = yaml.load(yml_file, Loader=yaml.Loader).get(data_name, {})

    if types == {}:
        logging.info('Empty dtypes fond in {}[{}]'.format(path, data_name))

    return types
