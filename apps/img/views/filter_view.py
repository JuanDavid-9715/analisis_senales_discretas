from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def low_pass_filter_view(request):
    """
    Vista para aplicar filtro pasa bajos
    """
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        
        # Llamar a la función de filtro pasa bajos
        # filtered_image, fft_filtered = apply_low_pass_filter(filename)
        
        context = {
            'title': 'Filtro Pasa Bajos',
            'filter_type': 'low_pass',
            'image_uploaded': True,
            'original_image': filename,
            # 'filtered_image': filtered_image,
            # 'fft_image': fft_filtered
        }
        return render(request, 'img/filters.html', context)
    
    context = {
        'title': 'Filtro Pasa Bajos',
        'filter_type': 'low_pass',
        'image_uploaded': False
    }
    return render(request, 'img/filters.html', context)

def high_pass_filter_view(request):
    """
    Vista para aplicar filtro pasa altos
    """
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        
        # Llamar a la función de filtro pasa altos
        # filtered_image, fft_filtered = apply_high_pass_filter(filename)
        
        context = {
            'title': 'Filtro Pasa Altos',
            'filter_type': 'high_pass',
            'image_uploaded': True,
            'original_image': filename,
            # 'filtered_image': filtered_image,
            # 'fft_image': fft_filtered
        }
        return render(request, 'img/filters.html', context)
    
    context = {
        'title': 'Filtro Pasa Altos',
        'filter_type': 'high_pass',
        'image_uploaded': False
    }
    return render(request, 'img/filters.html', context)

def band_pass_filter_view(request):
    """
    Vista para aplicar filtro pasa bandas
    """
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        
        # Llamar a la función de filtro pasa bandas
        # filtered_image, fft_filtered = apply_band_pass_filter(filename)
        
        context = {
            'title': 'Filtro Pasa Bandas',
            'filter_type': 'band_pass',
            'image_uploaded': True,
            'original_image': filename,
            # 'filtered_image': filtered_image,
            # 'fft_image': fft_filtered
        }
        return render(request, 'img/filters.html', context)
    
    context = {
        'title': 'Filtro Pasa Bandas',
        'filter_type': 'band_pass',
        'image_uploaded': False
    }
    return render(request, 'filters.html', context)