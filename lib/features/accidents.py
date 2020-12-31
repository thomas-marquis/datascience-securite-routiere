import logging

import pandas as pd

from lib.constant import Datasets
from lib.features.dtypes import dtypes_clean, dtypes_featured


# features computing functions
def _compute_acc_severity(acc_severities: pd.Series) -> str:
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


# build new datasets
def build_accidents_dataset(caracs: pd.DataFrame,
                            locations: pd.DataFrame,
                            users: pd.DataFrame,
                            dtypes_base_path: str = '') -> pd.DataFrame:
    logging.info('merge caracs with locations (1 accident = 1 carac = 1 location)')
    acc_df = pd.merge(caracs, locations, on='Num_Acc', how='inner')

    logging.info('add nb victims by severity (4 columns)')
    vict_by_severity_cnt = pd.merge(caracs, users, on='Num_Acc', how='inner') \
        .groupby(by=['Num_Acc', 'grav']).count().reset_index()[['Num_Acc', 'grav', 'year']] \
        .rename({'year': 'victims_nb'}, axis=1) \
        .fillna({'victims_nb': 0}) \
        .pivot(index='Num_Acc', columns='grav')
    vict_by_severity_cnt.columns = vict_by_severity_cnt.columns.get_level_values(1)
    vict_by_severity_cnt.rename(columns=str).reset_index()
    acc_df = pd.merge(acc_df, vict_by_severity_cnt, on='Num_Acc', how='inner')

    logging.info('add total victims number column')
    victims_nb_by_acc = pd.merge(caracs, users, on='Num_Acc', how='inner') \
        .groupby(by=['Num_Acc']).count().reset_index()[['Num_Acc', 'year']] \
        .rename({'year': 'victims_nb'}, axis=1)
    acc_df = pd.merge(acc_df, victims_nb_by_acc, on='Num_Acc', how='inner')

    logging.info('add acc_severity column')
    acc_severity = pd.merge(acc_df, users, on='Num_Acc', how='inner') \
        .loc[:, ['Num_Acc', 'grav']] \
        .groupby(by='Num_Acc') \
        .agg(acc_severity=pd.NamedAgg(column='grav', aggfunc=_compute_acc_severity)) \
        .reset_index() \
        .astype({'acc_severity': 'category', 'Num_Acc': 'string'})
    acc_df = pd.merge(acc_df, acc_severity, on='Num_Acc', how='inner')

    return acc_df.astype(dtypes_featured(Datasets.ACCIDENTS, base_path=dtypes_base_path))


def build_victims_dataset(caracs: pd.DataFrame,
                          users: pd.DataFrame,
                          dtypes_base_path: str = '') -> pd.DataFrame:
    victims = pd.merge(caracs, users, on='Num_Acc', how='inner')

    # age
    victims['age'] = victims['year'] - victims['an_nais']

    return victims.astype(dtypes_clean('victims', base_path=dtypes_base_path))
