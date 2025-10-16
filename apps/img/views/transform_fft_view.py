from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from ..forms import GraysCaleForm
from ..utils.grayscale import GrayscaleProcessor


def grayscale_view(request):
    """
    Vista para conversión a escala de grises
    """

    if request.method == 'GET':
        return render(request, 'transform_fft.html', {
            'image_uploaded': False,
            'img_form': GraysCaleForm()
        })

    if request.method == 'POST':
        form = GraysCaleForm(request.POST, request.FILES)
        
        if form.is_valid():
            fs = FileSystemStorage()
            
            # Guardar nueva imagen SOLO si se envió una
            if 'img' in request.FILES and request.FILES['img']:
                # Eliminar imágenes anteriores si existen
                for filename in ["original_image.jpg", "grayscale_image.jpg", "fft_image.jpg"]:
                    if fs.exists(filename):
                        fs.delete(filename)
                
                # Guardar nueva imagen
                uploaded_file = form.cleaned_data['img']
                fs.save("original_image.jpg", uploaded_file)
            
            try:
                # Aplicar conversión a escala de grises
                processor = GrayscaleProcessor()
                process_name = processor.apply_grayscale()
                
                return render(request, 'transform_fft.html', {
                    'image_uploaded': True,
                    'img_form': GraysCaleForm(),
                    'process_name': process_name
                })
                
            except Exception as e:
                return render(request, 'transform_fft.html', {
                    'image_uploaded': False,
                    'img_form': form,
                    'error_message': f'Error al procesar la imagen: {str(e)}'
                })
        
        # Si el formulario no es válido
        return render(request, 'transform_fft.html', {
            'image_uploaded': False,
            'img_form': form
        })