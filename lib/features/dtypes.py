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
        'adr': 'string',
        'lat': 'string',
        'long': 'string',
        'datetime': 'datetime64[ns]',
        'year': 'Int32',
        'month': 'Int32',
        'day': 'Int32',
        'hour': 'Int32',
        'weekday': 'Int32',
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
            'lartpc': 'float32',
            'pr': 'float32',
            'pr1': 'float32',
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
