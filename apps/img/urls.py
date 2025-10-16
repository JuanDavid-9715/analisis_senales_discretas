from django.urls import path
from .views.transform_fft_view import grayscale_view
from .views.filter_view import filter_view
from .views.compression_view import compression_view


urlpatterns = [
    # Transformaciones
    path('grayscale/', grayscale_view, name='grayscale'),
    # Filtros
    path('filters/', filter_view, name='filter'),
    # Compresión
    path('compression/', compression_view, name='compression'),
]
