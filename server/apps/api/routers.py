from django.urls import path

from apps.api.viewsets import PointView
from apps.analysis.build_data import import_data_to_db, import_points_to_db, \
    import_data_to_csv, get_database_size, process_point_values

from .viewsets import RouterBuilder

app_name = 'api'

urlpatterns = [
    path('points/', PointView.as_view()),
    path('import_data_to_db/', import_data_to_db),
    path('import_data_to_csv/', import_data_to_csv),
    path('import_points_to_db/', import_points_to_db),
    path('get_route/', RouterBuilder.as_view()),
    path('get_database_size/', get_database_size),
    path('process_points/', process_point_values),
]
