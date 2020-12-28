import logging

import pandas as pd


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
    :return: index=df columns, columns=`['na_count', 'na_rate']`
    """

    nas = []
    for col in df.columns:
        na_count = df[col].isna().sum()
        na_rate = na_count / df.shape[0]
        nas.append({'na_count': na_count, 'na_rate': na_rate})

        logging.info('{}: {:.2f}% NA'.format(col, na_rate * 100))

    return pd.DataFrame(nas, index=df.columns)
