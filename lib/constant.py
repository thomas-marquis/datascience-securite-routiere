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


class Datasets(Constant):
    CARACS = 'caracs'
    USERS = 'users'
    LOCATIONS = 'locations'
    VEHICLES = 'vehicles'