from django.urls import path
from .views.views import index
from .views.transform_fft_view import grayscale_view
from .views.filter_view import low_pass_filter_view, high_pass_filter_view, band_pass_filter_view
from .views.compression_view import image_compression_view, ibp_compression_view

urlpatterns = [
    path('', index, name='index'),
    
    # Transformaciones
    path('transform/grayscale/', grayscale_view, name='grayscale'),

    
    # Filtros
    path('filters/low-pass/', low_pass_filter_view, name='low_pass_filter'),
    path('filters/high-pass/', high_pass_filter_view, name='high_pass_filter'),
    path('filters/band-pass/', band_pass_filter_view, name='band_pass_filter'),
    
    # Compresión
    path('compression/basic/', image_compression_view, name='image_compression'),
    path('compression/ibp/', ibp_compression_view, name='ibp_compression'),
]
