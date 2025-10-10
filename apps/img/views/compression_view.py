from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def image_compression_view(request):
    """
    Vista para compresión básica de imágenes
    """
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        compression_percentage = request.POST.get('compression_percentage', 50)
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        
        # Llamar a la función de compresión
        # compressed_image, image_weight = compress_image(filename, compression_percentage)
        
        context = {
            'title': 'Compresión de Imagen',
            'compression_type': 'basic',
            'image_uploaded': True,
            'original_image': filename,
            'compression_percentage': compression_percentage,
            # 'compressed_image': compressed_image,
            # 'image_weight': image_weight
        }
        return render(request, 'img/compression.html', context)
    
    context = {
        'title': 'Compresión de Imagen',
        'compression_type': 'basic',
        'image_uploaded': False
    }
    return render(request, 'img/compression.html', context)

def ibp_compression_view(request):
    """
    Vista para compresión IBP (Iterative Back Projection)
    """
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        
        # Llamar a la función de compresión IBP
        # compressed_image, image_weight = apply_ibp_compression(filename)
        
        context = {
            'title': 'Compresión IBP',
            'compression_type': 'ibp',
            'image_uploaded': True,
            'original_image': filename,
            # 'compressed_image': compressed_image,
            # 'image_weight': image_weight
        }
        return render(request, 'img/compression.html', context)
    
    context = {
        'title': 'Compresión IBP',
        'compression_type': 'ibp',
        'image_uploaded': False
    }
    return render(request, 'compression.html', context)
