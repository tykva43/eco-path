import os

import pandas as pd

import requests

from apps.db.business_logic import PointWrapper, MeasureWrapper
from rest_framework import status
from rest_framework.response import Response

from .config import ORIGIN_DATA_PATH_CSV, ALL_MEASURE_FILENAME


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
    i = 0
    for filename in file_list:
        print(filename)
        chunksize = 10 ** 6
        street = filename[:filename.find('_')]
        house = filename[filename.find('_') + 1:filename.find('.')]
        lat, lon = get_coordinates_by_address('Москва ' + street + ' ' + house)
        for chunk in pd.read_csv(dir_path + filename, chunksize=chunksize, header=0,
                                 names=['date', 'temp', 'wet', 'CO2',
                                        'LOS', 'dust_pm_1',
                                        'dust_pm_2_5', 'dust_pm_10', 'pressure',
                                        'AQI', 'formaldehyde']):
            chunk['lat'] = lat
            chunk['lon'] = lon
            if not i:
                chunk.to_csv(dir_path + ALL_MEASURE_FILENAME)
                i = 1
            else:
                chunk.to_csv(dir_path + ALL_MEASURE_FILENAME, header=None, mode='a')
    print('************ready**************')


def collect_points(dir_path=ORIGIN_DATA_PATH_CSV):
    file_list = os.listdir(dir_path)
    points_list = []
    for filename in file_list:
        street = filename[:filename.find('_')]
        house = filename[filename.find('_') + 1:filename.find('.')]
        lat, lon = get_coordinates_by_address('Москва ' + street + ' ' + house)
        points_list.append({'lat': lat, 'lon': lon})
        print(filename)
    print('saved all points')
    PointWrapper.bulk_create(points_list)


def import_points_to_db(request):
    PointWrapper.clear()
    collect_points()


def import_data_to_db(request):
    MeasureWrapper.clear()
    collect_from_dir()
    return Response(status=status.HTTP_200_OK)
