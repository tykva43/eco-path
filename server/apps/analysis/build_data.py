import os

import pandas as pd

import random

import requests

from apps.db.business_logic import PointWrapper, MeasureWrapper
from .config import PREPARED_PATH, ORIGIN_DATA_PATH


def get_coordinates_by_address(address):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        'q': address,
        'debug': True,
        'key': 'e4c820ba-37c0-4801-9bba-3b559cea39ab',
        'locale': 'ru',
    }
    response = requests.get(url=url, params=params)
    response = response.json()
    point_data = response['data']['hits'][0]['point']
    return point_data['lat'], point_data['lng']


def collect_from_dir(req, dir_path=ORIGIN_DATA_PATH):
    file_list = os.listdir(dir_path)
    for filename in file_list:
        print('Box ' + filename[:filename.find('.')])
        df = pd.read_excel(dir_path + filename, header=None, engine='openpyxl')
        # df = pd.read_excel(dir_path + filename, header=None, sheet_name='Box ' + filename[:filename.find('.')], index_col=None)
        address = filename[:filename.find('_')]

        print(df.head())
        lat, lon = get_coordinates_by_address('Москва ' + address)
        PointWrapper.save({'lat': lat, 'lon': lon})
        df.loc[df, 'lat'] = lat
        df.loc[df, 'lon'] = lon
        MeasureWrapper.bulk_update(df.loc[df, ~df.columns.str.contains('^Unnamed')].to_dict())
    return file_list

    # df = pd.read_csv(ORIGIN_DATA_FILEPATH)
    #
    # for i in range(len(df)):
    #     df.loc[i, 'point_type'] = 'П'
    #     df.loc[i, 'characteristics'] = ','.join(map(str, random.sample(SAMPLE_CHOICES, random.randint(0, 5))))
    # print(df.head())
    # df.to_csv(PREPARED_FILEPATH)


def collect_from_file(filename):
    ...
    # curl "https://graphhopper.com/api/1/geocode?q=berlin&locale=de&debug=true&key=api_key"
    # l = []
    # for i in range(len(df)):
    #     l.append(df.loc[i, ~df.columns.str.contains('^Unnamed')].to_dict())
    # return l

# def import_data_to_db():
#     df = pd.read_csv(PREPARED_FILEPATH)
#     PointWrapper.bulk_save(df_to_list(df))


# def recreate_data(request):
#     generate_random_data()
#     PointWrapper.clear_all()
#     import_data_to_db()
#     return JsonResponse({'info': 'ready'})


# def create_db(request):
#     PeopleTypeWrapper.save({'requirements': [1, 2, 3], 'name': 'Слабовидящий человек'})
#     PeopleTypeWrapper.save({'requirements': [1, 3, 5], 'name': 'Передвижение на коляске'})
#     # PeopleTypeWrapper.save({'requirements': [1, 3, 4, 2, 5], 'name': 'Другое'})
#     DisabilityRequirementWrapper.save({'name': 'Пандусы/пониженные бордюры'})
#     DisabilityRequirementWrapper.save({'name': 'Остановки общественного транспорта'})
#     DisabilityRequirementWrapper.save({'name': 'Твердое дорожное покрытие'})
#     DisabilityRequirementWrapper.save({'name': 'Светофор со звуковым сигналом'})
#     DisabilityRequirementWrapper.save({'name': 'Ширина тротуара не менее 1м'})
#     return JsonResponse({'info': 'ready'})
