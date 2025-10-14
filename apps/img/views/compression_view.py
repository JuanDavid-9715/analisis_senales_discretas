from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from ..forms import CompressionForm
from ..utils.compression import ImageCompressionProcessor


def compression_view(request):
    """
    Vista para compresión de imágenes
    """

    if request.method == 'GET':
        return render(request, 'compression.html', {
            'image_uploaded': False,
            'compression_form': CompressionForm()
        })

    if request.method == 'POST':
        print("se envio un POST de compresión")
        form = CompressionForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("form de compresión es valido")
            fs = FileSystemStorage()
            
            # Guardar nueva imagen SOLO si se envió una
            if 'img' in request.FILES and request.FILES['img']:
                print("se envio una imagen para compresión")
                # Eliminar imágenes anteriores si existen
                for filename in ["original_image.jpg", "compressed_image.jpg", "lbp_image.jpg"]:
                    if fs.exists(filename):
                        fs.delete(filename)
                
                # Guardar nueva imagen
                uploaded_file = form.cleaned_data['img']
                fs.save("original_image.jpg", uploaded_file)
            
            # Obtener parámetros y procesar
            compression_percentage = form.cleaned_data['compression_percentage']
            
            print(f"Porcentaje de compresión: {compression_percentage}%")
            
            try:
                # Aplicar compresión
                processor = ImageCompressionProcessor()
                compression_info = processor.apply_compression(compression_percentage)
                
                return render(request, 'compression.html', {
                    'image_uploaded': True,
                    'compression_form': CompressionForm(initial={
                        'compression_percentage': compression_percentage
                    }),
                    'compression_info': compression_info
                })
                
            except Exception as e:
                return render(request, 'compression.html', {
                    'image_uploaded': False,
                    'compression_form': form,
                    'error_message': f'Error al comprimir la imagen: {str(e)}'
                })
        
        # Si el formulario no es válido
        return render(request, 'compression.html', {
            'image_uploaded': False,
            'compression_form': form
        })