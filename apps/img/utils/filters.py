import os
import numpy as np
from PIL import Image
from io import BytesIO
from django.core.files.storage import FileSystemStorage

class ImageFilterProcessor:
    """
    Clase para procesar filtros de frecuencia en imágenes usando PIL
    """
    
    def __init__(self):
        self.fs = FileSystemStorage()
    
    def apply_filter(self, filter_type, cutoff=30, cutoff2=60):
        """
        Aplica filtros en el dominio de la frecuencia
        """
        # Cargar imagen original con PIL
        img = self._load_image_pil("original_image.jpg")
        
        if img is None:
            raise ValueError("No se pudo cargar la imagen original")
        
        # Calcular FFT
        F = np.fft.fft2(img)
        Fshift = np.fft.fftshift(F)
        
        # Aplicar filtro según el tipo
        if filter_type == 'low_pass':
            mask = self._filtro_pasabajos(img.shape, cutoff)
        elif filter_type == 'high_pass':
            mask = self._filtro_pasaaltos(img.shape, cutoff)
        elif filter_type == 'band_pass':
            mask = self._filtro_pasabanda(img.shape, cutoff, cutoff2)
        else:
            raise ValueError("Tipo de filtro no válido")
        
        # Aplicar máscara en el dominio de la frecuencia
        F_filtered = Fshift * mask
        
        # Reconstruir imagen filtrada
        img_filtered = np.abs(np.fft.ifft2(np.fft.ifftshift(F_filtered)))
        
        # Calcular FFT de la imagen filtrada para visualización
        F_filtered_fft = np.fft.fft2(img_filtered)
        F_filtered_shift = np.fft.fftshift(F_filtered_fft)
        magnitude_spectrum = np.log(1 + np.abs(F_filtered_shift))
        
        # Guardar imágenes
        self._save_image_pil(img_filtered, "filtered_image.jpg")
        self._save_image_pil(magnitude_spectrum, "fft_image.jpg")
        
        # Retornar nombre del filtro aplicado
        if filter_type == 'low_pass':
            return f"Pasa Bajos (cutoff={cutoff})"
        elif filter_type == 'high_pass':
            return f"Pasa Altos (cutoff={cutoff})"
        elif filter_type == 'band_pass':
            return f"Pasa Banda ({cutoff}-{cutoff2})"
    
    def _load_image_pil(self, filename):
        """Cargar imagen usando PIL"""
        try:
            img_path = self.fs.path(filename)
            
            if not os.path.exists(img_path):
                return None
            
            # Cargar con PIL
            imagen = Image.open(img_path)
            
            # Convertir a escala de grises si es necesario
            if imagen.mode != 'L':
                imagen = imagen.convert('L')
            
            # Convertir a numpy array
            imagen_array = np.array(imagen)
            
            return imagen_array
            
        except Exception:
            return None
    
    def _filtro_pasabajos(self, shape, radio):
        """Filtro pasa bajos"""
        filas, cols = shape
        crow, ccol = filas//2, cols//2
        y, x = np.ogrid[:filas, :cols]
        mask = ((x - ccol)**2 + (y - crow)**2 <= radio**2).astype(np.uint8)
        return mask
    
    def _filtro_pasaaltos(self, shape, radio):
        """Filtro pasa altos"""
        filas, cols = shape
        crow, ccol = filas//2, cols//2
        y, x = np.ogrid[:filas, :cols]
        mask = ((x - ccol)**2 + (y - crow)**2 > radio**2).astype(np.uint8)
        return mask
    
    def _filtro_pasabanda(self, shape, r_in, r_out):
        """Filtro pasa banda"""
        filas, cols = shape
        crow, ccol = filas//2, cols//2
        y, x = np.ogrid[:filas, :cols]
        distance = (x - ccol)**2 + (y - crow)**2
        mask = ((distance <= r_out**2) & (distance > r_in**2)).astype(np.uint8)
        return mask
    
    def _save_image_pil(self, image, filename):
        """Guardar imagen usando PIL y FileSystemStorage"""
        try:
            # Normalizar imagen a 0-255
            if image.dtype != np.uint8:
                image_min = image.min()
                image_max = image.max()
                if image_max > image_min:
                    image_normalized = ((image - image_min) / (image_max - image_min) * 255).astype(np.uint8)
                else:
                    image_normalized = np.zeros_like(image, dtype=np.uint8)
            else:
                image_normalized = image
            
            # Convertir a PIL Image
            pil_image = Image.fromarray(image_normalized)
            
            # Crear un buffer en memoria
            buffer = BytesIO()
            
            # Guardar la imagen en el buffer como JPEG
            pil_image.save(buffer, format='JPEG', quality=95)
            
            # Mover el cursor al inicio del buffer
            buffer.seek(0)
            
            # Eliminar archivo existente si existe
            if self.fs.exists(filename):
                self.fs.delete(filename)
            
            # Guardar usando FileSystemStorage con el buffer
            self.fs.save(filename, buffer)
            
        except Exception as e:
            raise ValueError(f"Error al guardar la imagen: {str(e)}")