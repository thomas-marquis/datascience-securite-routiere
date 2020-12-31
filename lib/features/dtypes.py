from lib import utils
from lib.constant import Datasets

clean_dtypes_file_path = 'resources/dtypes/cleaned.yml'


def dtypes_clean(data_name: str, base_path: str = '') -> dict:
    assert data_name in Datasets.list_all()

    return utils.get_dtypes(data_name, clean_dtypes_file_path, base_path=base_path)
