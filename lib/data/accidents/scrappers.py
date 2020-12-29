from typing import Dict

from lib.constant import Datasets

urls = {
    Datasets.CARACS: {
        2019: 'https://www.data.gouv.fr/fr/datasets/r/e22ba475-45a3-46ac-a0f7-9ca9ed1e283a',
        2018: 'https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405',
        2017: 'https://www.data.gouv.fr/fr/datasets/r/9a7d408b-dd72-4959-ae7d-c854ec505354',
        2016: 'https://www.data.gouv.fr/fr/datasets/r/96aadc9f-0b55-4e9a-a70e-c627ed97e6f7',
    },
    Datasets.LOCATIONS: {
        2019: 'https://www.data.gouv.fr/fr/datasets/r/2ad65965-36a1-4452-9c08-61a6c874e3e6',
        2018: 'https://www.data.gouv.fr/fr/datasets/r/d9d65ca1-16a3-4ea3-b7c8-2412c92b69d9',
        2017: 'https://www.data.gouv.fr/fr/datasets/r/9b76a7b6-3eef-4864-b2da-1834417e305c',
        2016: 'https://www.data.gouv.fr/fr/datasets/r/08b77510-39c4-4761-bf02-19457264790f',
    },
    Datasets.VEHICLES: {
        2019: 'https://www.data.gouv.fr/fr/datasets/r/780cd335-5048-4bd6-a841-105b44eb2667',
        2018: 'https://www.data.gouv.fr/fr/datasets/r/b4aaeede-1a80-4d76-8f97-543dad479167',
        2017: 'https://www.data.gouv.fr/fr/datasets/r/d6103d0c-6db5-466f-b724-91cbea521533',
        2016: 'https://www.data.gouv.fr/fr/datasets/r/be2191a6-a7cd-446f-a9fc-8d698688eb9e',
    },
    Datasets.USERS: {
        2019: 'https://www.data.gouv.fr/fr/datasets/r/36b1b7b3-84b4-4901-9163-59ae8a9e3028',
        2018: 'https://www.data.gouv.fr/fr/datasets/r/72b251e1-d5e1-4c46-a1c2-c65f1b26549a',
        2017: 'https://www.data.gouv.fr/fr/datasets/r/07bfe612-0ad9-48ef-92d3-f5466f8465fe',
        2016: 'https://www.data.gouv.fr/fr/datasets/r/e4c6f4fe-7c68-4a1d-9bb6-b0f1f5d45526',
    },
}


def get_urls_by_dataset() -> Dict[str, Dict[int, str]]:
    """Scrap data.gouv and return url dict.

    returned dict structure::

        {
            'dataset_name': {
                XXXX: 'url'
            }
        }

    **dataset_name** in `['carac', 'lieux', 'usag', 'veh']`

    **XXXX** year int
    """
    return urls
