import pandas as pd


def get_drivers_count(pop_sex: pd.DataFrame, entd: pd.DataFrame) -> pd.DataFrame:
    # on récupère la taille de la population en age de conduire (par an)
    # (> 20 ans à défaut d'avoir la tranche d'âge > 18 ans)
    drivers_count = pop_sex\
        .rename({'Annee': 'year', 'Hommes': 'pop_male', 'Femmes': 'pop_female'}, axis=1)\
        .loc[pop_sex['Tranches'].str.contains('|'.join(['20 à 64 ans', '65 ans ou plus'])),
             ['pop_male', 'pop_female', 'year']]\
        .groupby(by=['year']).sum().reset_index()

    # on corrige ce nombre par la proportion (estimée par l'ENTD) de personnes ayant le permi
    drivers_count['permi_male'] = drivers_count['pop_male'] * \
        (entd.loc['ENSEMBLE', 'Homme Titulaire du permis'] / 100)
    drivers_count['permi_female'] = drivers_count['pop_female'] * \
        (entd.loc['ENSEMBLE', 'Femme Titulaire du permis'] / 100)

    # on corrige ce nombre par la proportion (estimée par l'ENTD) de personnes ayant le permi et conduisant
    drivers_count['drive_male'] = drivers_count['permi_male'] * \
        (entd.loc['ENSEMBLE', 'Homme Conduit'] / 100)
    drivers_count['drive_female'] = drivers_count['permi_female'] * \
        (entd.loc['ENSEMBLE', 'Femme Conduit'] / 100)
    drivers_count['drive_tot'] = drivers_count['drive_male'] + \
        drivers_count['drive_female']

    # enfin, on calcul les proportions de conducteurs actifs H/F
    drivers_count['prop_drive_male'] = drivers_count['drive_male'] / \
        drivers_count['drive_tot']
    drivers_count['prop_drive_female'] = drivers_count['drive_female'] / \
        drivers_count['drive_tot']

    # On fait le ménage dans les colonnes
    drivers_count = drivers_count.drop(['pop_male',
                                        'pop_female',
                                        'permi_male',
                                        'permi_female',
                                        'drive_male',
                                        'drive_female',
                                        'drive_tot'], axis=1)

    return drivers_count
