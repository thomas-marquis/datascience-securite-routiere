# utilities
class Constant:
    @classmethod
    def list_all(cls):
        return [v for k, v in cls.__dict__.items() if not k.startswith('_')]


# constants
to_csv_kwargs = {
    'sep': ';',
    'header': True,
    'index': False,
}

read_csv_kwargs = {
    'sep': ';',
    'header': 0,
}


class Datasets(Constant):
    # base datasets
    CARACS = 'caracs'
    USERS = 'users'
    LOCATIONS = 'locations'
    VEHICLES = 'vehicles'

    # created datasets
    ACCIDENTS = 'accidents'
