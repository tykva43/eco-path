import os

import pandas as pd

import requests
import psycopg2

from apps.db.business_logic import PointWrapper, MeasureWrapper
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from .config import ORIGIN_DATA_PATH_CSV, ALL_MEASURE_FILENAME, POINTS_VALUES_FILENAME


def get_coordinates_by_address(address):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        'q': address,
        'debug': True,
        'key': 'e4c820ba-37c0-4801-9bba-3b559cea39ab',
        'locale': 'ru',
        'algorithm': 'alternative_route',
        'alternative_route': {'max_paths': 5},
    }
    response = requests.get(url=url, params=params)
    response = response.json()
    point_data = response['hits'][0]['point']
    return point_data['lat'], point_data['lng']


def collect_from_dir(dir_path=ORIGIN_DATA_PATH_CSV):
    file_list = os.listdir(dir_path)
    try:
        file_list.remove(ALL_MEASURE_FILENAME)
    except ValueError:
        pass
    i = 0
    counter = 0
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
                                        'AQI', 'formaldehyde'], index_col=False):
            chunk['point'] = PointWrapper.find_by_coords(lat, lon).id
            chunk['date'] = pd.to_datetime(chunk.date)
            chunk.insert(0, "id", range(counter, counter + len(chunk)))
            chunk.fillna(0)
            chunk.loc[chunk['dust_pm_1'].isnull(), 'dust_pm_1'] = .0
            chunk.loc[chunk['dust_pm_2_5'].isnull(), 'dust_pm_2_5'] = .0
            chunk.loc[chunk['dust_pm_10'].isnull(), 'dust_pm_10'] = .0
            chunk.loc[chunk['pressure'].isnull(), 'pressure'] = .0
            chunk.loc[chunk['formaldehyde'].isnull(), 'formaldehyde'] = .0
            chunk.loc[chunk['LOS'].isnull(), 'LOS'] = .0
            chunk.loc[chunk['AQI'].isnull(), 'AQI'] = .0
            chunk.loc[chunk['CO2'].isnull(), 'CO2'] = .0
            chunk.loc[chunk['wet'].isnull(), 'wet'] = .0
            counter += len(chunk)
            # chunk['date'] = chunk['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            if not i:
                chunk.to_csv(dir_path + ALL_MEASURE_FILENAME, header=None, index=False)
                i = 1
            else:
                chunk.to_csv(dir_path + ALL_MEASURE_FILENAME, header=None, mode='a', index=False)
    print('************ready**************')


def collect_points(dir_path=ORIGIN_DATA_PATH_CSV):
    file_list = os.listdir(dir_path)
    try:
        file_list.remove(ALL_MEASURE_FILENAME)
    except ValueError:
        pass
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


def import_data_to_csv(request):
    collect_from_dir()
    return Response({'info': 'ok'}, status=status.HTTP_200_OK)


from urllib.parse import urlparse


def import_data_to_db(request):
    MeasureWrapper.clear()
    f_contents = open(ORIGIN_DATA_PATH_CSV + ALL_MEASURE_FILENAME, 'r')
    # postgres://postgres:postgres@db:5432/postgres
    result = urlparse("postgres://postgres:postgres@db:5432/postgres")

    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    connection = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    db_cursor = connection.cursor()
    db_cursor.copy_from(f_contents, "db_measure", sep=",")
    connection.commit()
    connection.close()
    return Response()


def get_database_size(req):
    result = urlparse("postgres://postgres:postgres@db:5432/postgres")

    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    connection = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    db_cursor = connection.cursor()
    db_cursor.execute("SELECT pg_size_pretty(pg_database_size('postgres'));")
    return JsonResponse({'data': db_cursor.fetchone()})


def process_point_values(request):
    dir_path = ORIGIN_DATA_PATH_CSV
    file_list = os.listdir(dir_path)
    try:
        file_list.remove(ALL_MEASURE_FILENAME)
    except ValueError:
        pass
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
                                        'AQI', 'formaldehyde'], index_col=False):

            chunk.loc[chunk['AQI'].isnull(), 'AQI'] = .0
            chunk['date'] = pd.to_datetime(chunk.date)
            chunk['point'] = PointWrapper.find_by_coords(lat, lon).id
            means = chunk.groupby(by=[chunk['date'].dt.day]).mean('AQI')
            mean = means["AQI"].mean()
            point = PointWrapper.find_by_coords(lat, lon)
            point.value = mean
            point.save()
    print('************ready**************')
    return JsonResponse({'info': 'ok'})
