from django.core.files.storage import FileSystemStorage
import numpy as np
from PIL import Image, ImageOps
from io import BytesIO

class GrayscaleProcessor:
    def __init__(self):
        self.fs = FileSystemStorage()
    
    def apply_grayscale(self):
        """
        Convierte una imagen RGB a escala de grises y calcula su Transformada de Fourier centrada.
        Guarda las imágenes con nombres fijos.
        Retorna: nombre del proceso completado
        """
        # Verificar que existe la imagen original
        if not self.fs.exists("original_image.jpg"):
            raise Exception("No existe imagen original para procesar")
        
        # Cargar imagen original
        original_path = self.fs.path("original_image.jpg")
        pil_img = Image.open(original_path)
        
        # Procesar imagen a escala de grises
        img_rgb = pil_img.convert("RGB")
        gray = ImageOps.grayscale(img_rgb)
        
        # Calcular FFT
        arr = np.asarray(gray).astype(np.float32)
        fft = np.fft.fft2(arr)
        fft_shift = np.fft.fftshift(fft)
        magnitude = np.log1p(np.abs(fft_shift)).astype(np.float32)
        
        # Guardar imagen en escala de grises
        gray_buffer = BytesIO()
        gray.save(gray_buffer, format='JPEG')
        gray_buffer.seek(0)
        self.fs.save("grayscale_image.jpg", gray_buffer)
        
        # Guardar imagen FFT (convertir numpy array a PIL Image)
        magnitude_normalized = (magnitude - magnitude.min()) / (magnitude.max() - magnitude.min()) * 255
        magnitude_img = Image.fromarray(magnitude_normalized.astype(np.uint8))
        
        fft_buffer = BytesIO()
        magnitude_img.save(fft_buffer, format='JPEG')
        fft_buffer.seek(0)
        self.fs.save("fft_image.jpg", fft_buffer)
        
        return "Conversión a escala de grises completada"