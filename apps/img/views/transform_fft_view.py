from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from ..forms import GraysCaleForm


def grayscale_view(request):
    """
    Vista para transformar imágenes de color a escala de grises
    """
    
    if request.method == 'POST':
        form = GraysCaleForm(request.POST, request.FILES)
        if form.is_valid():
            fs = FileSystemStorage()
            
            if fs.exists("original_image.jpg"):
                fs.delete("original_image.jpg")
                
            fs.save("original_image.jpg", form.cleaned_data['img'])
            
            process_grayscale()
            
            context = {
                'image_uploaded': True,
                'img_form': GraysCaleForm(),
            }
            
            return render(request, 'transform_fft.html', context)
    
    context = {
        'image_uploaded': False,
        'img_form': GraysCaleForm(),
    }
    
    return render(request, 'transform_fft.html', context)

def process_grayscale():
    pass