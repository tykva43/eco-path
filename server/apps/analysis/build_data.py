import os

import pandas as pd

import requests

from apps.db.business_logic import PointWrapper, MeasureWrapper
from rest_framework import status
from rest_framework.response import Response

from .config import ORIGIN_DATA_PATH_CSV


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
    point_data = response['hits'][0]['point']
    return point_data['lat'], point_data['lng']


def collect_from_dir(dir_path=ORIGIN_DATA_PATH_CSV):
    file_list = os.listdir(dir_path)
    for filename in file_list:
        df = pd.read_csv(dir_path+filename, header=0, names=['date', 'temp', 'wet', 'CO2', 'LOS', 'dust_pm_1',
                                                             'dust_pm_2_5', 'dust_pm_10', 'pressure',
                                                             'AQI', 'formaldehyde'], index_col=False)
        street = filename[:filename.find('_')]
        house = filename[filename.find('_')+1:filename.find('.')]

        lat, lon = get_coordinates_by_address('Москва ' + street + ' ' + house)
        PointWrapper.save({'lat': lat, 'lon': lon})
        df['lat'] = lat
        df['lon'] = lon
        l = [df.loc[i, ~df.columns.str.contains('^Unnamed')].to_dict() for i in range(len(df))]
        MeasureWrapper.bulk_create(l)
    return file_list


def import_data_to_db(request):
    PointWrapper.clear()
    MeasureWrapper.clear()
    collect_from_dir()
    return Response(status=status.HTTP_200_OK)


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
