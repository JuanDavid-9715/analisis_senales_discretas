from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from ..forms import FilterForm
from ..utils.filters import ImageFilterProcessor


def filter_view(request):
    """
    Vista para aplicar filtros de frecuencia
    """

    if request.method == 'GET':
        return render(request, 'filters.html', {
            'image_uploaded': False,
            'filter_form': FilterForm()
        })

    if request.method == 'POST':
        print("se envio un POST")
        form = FilterForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("form es valido")
            fs = FileSystemStorage()
            
            # Guardar nueva imagen SOLO si se envió una
            if 'img' in request.FILES and request.FILES['img']:
                print("se envio una imagen")
                # Eliminar imágenes anteriores si existen
                for filename in ["original_image.jpg", "filtered_image.jpg", "fft_image.jpg"]:
                    if fs.exists(filename):
                        fs.delete(filename)
                
                # Guardar nueva imagen
                uploaded_file = form.cleaned_data['img']
                fs.save("original_image.jpg", uploaded_file)
            
            # Obtener parámetros y procesar
            filter_type = form.cleaned_data['filter_type']
            cutoff = form.cleaned_data['cutoff']
            cutoff2 = form.cleaned_data['cutoff2']
            
            print(filter_type)
            print(cutoff)
            print(cutoff2)
            
            try:
                # Aplicar filtro
                processor = ImageFilterProcessor()
                filter_name = processor.apply_filter(filter_type, cutoff, cutoff2)
                
                return render(request, 'filters.html', {
                    'image_uploaded': True,
                    'filter_form': FilterForm(initial={
                        'filter_type': filter_type,
                        'cutoff': cutoff,
                        'cutoff2': cutoff2
                    }),
                    'filter_name': filter_name
                })
                
            except Exception as e:
                return render(request, 'filters.html', {
                    'image_uploaded': False,
                    'filter_form': form,
                    'error_message': f'Error al procesar la imagen: {str(e)}'
                })
        
        # Si el formulario no es válido
        return render(request, 'filters.html', {
            'image_uploaded': False,
            'filter_form': form
        })