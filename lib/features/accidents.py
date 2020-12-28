import logging

import pandas as pd


# dtypes
def dtypes(data_name: str) -> dict:
    users = {
        'Num_Acc': 'string',
        'num_veh': 'string',
        'place': 'category',
        'catu': 'category',
        'grav': 'category',
        'sexe': 'category',
        'an_nais': 'Int32',
        'trajet': 'category',
        'locp': 'category',
        'actp': 'category',
        'etatp': 'category',
    }
    caracs = {
        'Num_Acc': 'string',
        'lum': 'category',
        'dep': 'string',
        'com': 'string',
        'agg': 'category',
        'int': 'category',
        'atm': 'category',
        'col': 'category',
        'gps': 'category',
        'adr': 'string',
        'lat': 'string',
        'long': 'string',
        'datetime': 'datetime64[ns]',
        'year': 'Int32',
        'month': 'Int32',
        'day': 'Int32',
        'hour': 'Int32',
    }
    if data_name == 'caracs':
        return caracs
    elif data_name == 'locations':
        return {
            'Num_Acc': 'string',
            'catr': 'category',
            'voie': 'string',
            'circ': 'category',
            'nbv': 'Int32',
            'vosp': 'category',
            'prof': 'category',
            'plan': 'category',
            'surf': 'category',
            'infra': 'category',
            'situ': 'category',
        }
    elif data_name == 'vehicles':
        return {
            'Num_Acc': 'string',
            'num_veh': 'string',
            'senc': 'category',
            'catv': 'category',
            'obs': 'category',
            'obsm': 'category',
            'choc': 'category',
            'manv': 'category',
            'occutc': 'Int32',
        }
    elif data_name == 'users':
        return users
    elif data_name == 'victims':
        return {
            **users,
            **caracs,
            'age': 'Int32',
        }
    else:
        raise ValueError(data_name)


# data cleaning functions
def clean_caracs_dataset(raw_caracs: pd.DataFrame) -> pd.DataFrame:
    caracs = raw_caracs.copy()

    # time
    caracs: pd.DataFrame = pd.concat(
        [caracs, caracs.loc[:, 'hrmn'].str.extract(
            r'^(?P<hour>\d{1,2}):?(?P<minute>\d{2})$', expand=False)],
        axis=1) \
        .drop('hrmn', axis=1) \
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
    short_year_mask = caracs['year'].str.len() == 2
    caracs.loc[short_year_mask, 'year'] = '20' + caracs.loc[short_year_mask, 'year']
    caracs: pd.DataFrame = caracs.astype({'year': 'Int32'})

    # add datetime columns
    caracs['hour'] = caracs['hour'].fillna(0)
    caracs['minute'] = caracs['minute'].fillna(0)
    caracs['datetime'] = pd.to_datetime(
        caracs.loc[:, ['year', 'month', 'day', 'hour', 'minute']])
    caracs: pd.DataFrame = caracs.drop(['minute'], axis=1)

    return caracs


def clean_locations_dataset(raw_locations: pd.DataFrame) -> pd.DataFrame:
    locations = raw_locations.copy()

    locations = locations.drop(
        ['pr', 'pr1', 'v1', 'v2', 'larrout', 'lartpc', 'env1'], axis=1)

    return locations


def clean_users_dataset(raw_users: pd.DataFrame) -> pd.DataFrame:
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
    users = users.drop(['secu', 'id_vehicule', 'secu1', 'secu2', 'secu3'], axis=1)

    return users


def clean_vehicles_dataset(raw_vehicles: pd.DataFrame) -> pd.DataFrame:
    vehicles = raw_vehicles.copy()

    vehicles = vehicles.drop(['id_vehicule', 'motor'], axis=1)

    return vehicles


# build new datasets
def build_victims_dataset(caracs: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    victims = pd.merge(caracs, users, on='Num_Acc', how='inner')

    # age
    victims['age'] = victims['year'] - victims['an_nais']

    victims = victims.astype(dtypes('victims'))

    return victims


# features computing functions
def compute_acc_severity(acc_severities: pd.Series) -> str:
    """Groupby method.

    Return the worst victim state for each accident.
    """

    # all_severity in ['safe', inj_light', 'inj_hosp', 'killed']
    acc_severities_unique = acc_severities.unique()

    if 'killed' in acc_severities_unique:
        max_severity = 'killed'
    elif 'inj_hosp' in acc_severities_unique:
        max_severity = 'inj_hosp'
    elif 'inj_light' in acc_severities_unique:
        max_severity = 'inj_light'
    else:
        max_severity = 'safe'

    return max_severity


def get_acc_severity(acc: pd.DataFrame) -> pd.DataFrame:
    """Pour chaque accident, donne l'état du blessé le plus grave. C'est la gravité de l'accident.

    Peut prendre plus d'une minute.
    """

    acc_severity = acc.loc[:, ['Num_Acc', 'grav']] \
        .groupby(by='Num_Acc') \
        .agg(acc_severity=pd.NamedAgg(column='grav', aggfunc=compute_acc_severity)) \
        .reset_index() \
        .astype({'acc_severity': 'category', 'Num_Acc': 'string'})

    return acc_severity


def get_pct_drivers_by_sex(drivers_count: pd.DataFrame) -> pd.DataFrame:
    """Nombre de conducteur dans la population en pourcentage par sex."""

    pct_drivers_sex = drivers_count \
        .mean()[['prop_drive_male', 'prop_drive_female']] \
        .mul(100).round(1)

    return pct_drivers_sex


def get_summary_by_sex(drivers: pd.DataFrame, pct_drivers_sex: pd.DataFrame) -> pd.DataFrame:
    summary = pd.crosstab(index=drivers['acc_severity'],
                          columns=drivers['sexe'],
                          margins=True, normalize=0) \
        .mul(100).round(1) \
        .append(pd.DataFrame({'female': pct_drivers_sex['prop_drive_female'],
                              'male': pct_drivers_sex['prop_drive_male']},
                             index=['Prop. conducteurs'])) \
        .rename({'All': 'Tous accidents',
                 'killed': 'Acc. mortel',
                 'inj_light': 'Acc. leger',
                 'inj_hosp': 'Acc.grave'}, axis=0) \
        .rename({'female': 'Femmes', 'male': 'Hommes'}, axis=1)

    return summary


def get_drivers(acc_severity: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    """Retourne l'ensemble des conducteurs impliqué dans un accident.

    on ajoute à la table des usager la colonne correspondant au type d'accident
    dans lequel il est impliqué (= état de la victime la plus grave)
    on ne récupère de cette table que les usagers conducteurs
    """

    drivers = pd.merge(acc_severity, users.loc[users['catu'] == 'driver', :],
                       on='Num_Acc', how='left') \
                .loc[:, ['Num_Acc', 'acc_severity', 'sexe', 'trajet']]

    return drivers
