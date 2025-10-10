from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from ..forms.img import ImgForm


def grayscale_view(request):
    """
    Vista para transformar imágenes de color a escala de grises
    """
    
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            fs = FileSystemStorage()
            
            if fs.exists("original_image.jpg"):
                fs.delete("original_image.jpg")
                
            fs.save("original_image.jpg", form.cleaned_data['img'])
            
            # process_grayscale()
            
            context = {
                'image_uploaded': True,
                'img_form': ImgForm(),
            }
            
            return render(request, 'transform_fft.html', context)
    
    context = {
        'image_uploaded': False,
        'img_form': ImgForm(),
    }
    return render(request, 'transform_fft.html', context)
