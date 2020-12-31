import logging

import pandas as pd

from lib.constant import Datasets
from lib.features.dtypes import dtypes_clean


def clean_caracs_dataset(raw_caracs: pd.DataFrame, dtypes_base_path: str = '') -> pd.DataFrame:
    caracs = raw_caracs.copy()

    # time
    caracs: pd.DataFrame = pd.concat(
        [caracs, caracs.loc[:, 'hrmn'].str.extract(
            r'^(?P<hour>\d{1,2}):?(?P<minute>\d{2})$', expand=False)],
        axis=1) \
        .astype({
        'hour': 'Int32',
        'minute': 'Int32',
    })

    # year
    caracs: pd.DataFrame = caracs.rename(columns={
        'an': 'year',
        'jour': 'day',
        'mois': 'month',
    })
    logging.debug(caracs.columns)
    caracs.loc[caracs['year'].str.len() == 2, 'year'] = '20' + caracs.loc[caracs['year'].str.len() == 2, 'year']
    caracs.loc[caracs['year'].str.len() == 1, 'year'] = '200' + caracs.loc[caracs['year'].str.len() == 1, 'year']
    caracs: pd.DataFrame = caracs.astype({'year': 'Int32'})

    # add datetime columns
    caracs['hour'] = caracs['hour'].fillna(0)
    caracs['minute'] = caracs['minute'].fillna(0)
    caracs['datetime'] = pd.to_datetime(
        caracs.loc[:, ['year', 'month', 'day', 'hour', 'minute']])
    caracs['weekday'] = caracs['datetime'].dt.weekday

    # remove columns
    caracs: pd.DataFrame = caracs.drop(['minute', 'gps', 'hrmn'], axis=1)

    return caracs.astype(dtypes_clean(Datasets.CARACS, base_path=dtypes_base_path))


def clean_locations_dataset(raw_locations: pd.DataFrame, dtypes_base_path: str = '') -> pd.DataFrame:
    locations = raw_locations.copy()

    locations = locations.drop(
        ['v1', 'v2', 'larrout', 'env1'], axis=1)
    locations['catr'] = locations['catr'].cat.rename_categories({
        1: 'autoroute',
        2: 'route_nat',
        3: 'route_dep',
        4: 'voie_commu',
        5: 'no_public',
        6: 'parking',
        7: 'metrop_urb',
        9: 'others',
    })
    locations['voie'] = locations['voie'].fillna('')
    locations['infra'] = locations['infra'].fillna(-1)
    locations['situ'] = locations['situ'].fillna(-1)
    locations['lartpc'] = locations['lartpc'] \
        .fillna('0') \
        .astype('float32')
    locations['pr'] = locations['pr'] \
        .str.replace('(', '').str.replace(')', '') \
        .astype('float32', errors='ignore')
    locations['pr1'] = locations['pr1'] \
        .str.replace('(', '').str.replace(')', '') \
        .astype('float32', errors='ignore')

    return locations.astype(dtypes_clean(Datasets.LOCATIONS, base_path=dtypes_base_path))


def clean_users_dataset(raw_users: pd.DataFrame, dtypes_base_path: str = '') -> pd.DataFrame:
    users = raw_users.copy()

    users['grav'] = users['grav'].cat.rename_categories({
        1: 'safe',
        2: 'killed',
        3: 'inj_hosp',
        4: 'inj_light',
    })
    users['sexe'] = users['sexe'].cat.rename_categories({
        1: 'male',
        2: 'female',
    })
    users['catu'] = users['catu'].cat.rename_categories({
        1: 'driver',
        2: 'passenger',
        3: 'pedest',
        4: 'pedest_roll',
    })
    users.loc[users['trajet'] == -1, 'trajet'] = 0
    users['trajet'] = users['trajet'].cat.rename_categories({
        0: 'unknown',
        1: 'home_work',
        2: 'home_school',
        3: 'shopping',
        4: 'pro',
        5: 'leisure',
        9: 'other',
    })
    users['etatp'] = users['etatp'].fillna(-1)
    users['locp'] = users['locp'].fillna(-1)
    users['actp'] = users['actp'].cat.add_categories([-1])
    users['actp'] = users['actp'].fillna(-1)
    users = users.drop(['secu', 'id_vehicule', 'secu1', 'secu2', 'secu3'], axis=1)

    return users.astype(dtypes_clean(Datasets.USERS, base_path=dtypes_base_path))


def clean_vehicles_dataset(raw_vehicles: pd.DataFrame, dtypes_base_path: str = '') -> pd.DataFrame:
    vehicles = raw_vehicles.copy()

    vehicles = vehicles.drop(['id_vehicule', 'motor'], axis=1)

    return vehicles.astype(dtypes_clean(Datasets.VEHICLES, base_path=dtypes_base_path))
