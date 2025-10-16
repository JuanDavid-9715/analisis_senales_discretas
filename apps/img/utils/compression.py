import io
import numpy as np
from PIL import Image
from django.core.files.storage import FileSystemStorage
from io import BytesIO

class ImageCompressionProcessor:
    def __init__(self):
        self.fs = FileSystemStorage()
    
    def apply_compression(self, percentage):
        """
        Aplica ambos métodos de compresión en escala de grises.
        """
        # Verificar que existe la imagen original
        if not self.fs.exists("original_image.jpg"):
            raise Exception("No existe imagen original para procesar")
        
        # Cargar imagen original
        original_path = self.fs.path("original_image.jpg")
        pil_img = Image.open(original_path)
        
        # Convertir a escala de grises para AMBAS compresiones
        gray_img = pil_img.convert("L")
        
        # Compresión por porcentaje en escala de grises
        compressed_img, compressed_size = compress_image_by_percentage(gray_img, percentage)
        
        # Compresión IBP en escala de grises
        lbp_img, lbp_size = compress_ibp(gray_img)
        
        # Guardar imágenes comprimidas (mismos nombres siempre)
        self._save_compressed_image(compressed_img, "compressed_image.jpg")
        self._save_compressed_image(lbp_img, "lbp_image.jpg")
        
        # Retornar información de compresión
        return {
            'compressed': f"Compresión {percentage}% - {self._format_size(compressed_size)}",
            'lbp': f"Compresión IBP - {self._format_size(lbp_size)}"
        }
    
    def _save_compressed_image(self, pil_image, filename):
        """Guarda una imagen PIL en el filesystem de Django"""
        # Eliminar imagen anterior si existe
        if self.fs.exists(filename):
            self.fs.delete(filename)
            
        buffer = BytesIO()
        pil_image.save(buffer, format='JPEG', quality=85, optimize=True)
        buffer.seek(0)
        self.fs.save(filename, buffer)
    
    def _format_size(self, size_bytes):
        """Formatea el tamaño en bytes a formato legible"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"


# TUS FUNCIONES EXACTAS - SIN MODIFICACIONES
def compress_image_by_percentage(pil_img, percentage, out_format="JPEG"):
    """
    Reduce el tamaño de la imagen en un porcentaje dado.
    Entrada:
      - pil_img: imagen PIL (RGB o L)
      - percentage: porcentaje de tamaño deseado (0-100]
    Salida:
      (imagen_comprimida, tamaño_en_bytes)
    """
    if percentage <= 0 or percentage > 100:
        raise ValueError("El porcentaje debe estar en (0, 100].")
    scale = percentage / 100.0
    w, h = pil_img.size
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    compressed = pil_img.resize(new_size, resample=Image.LANCZOS)

    buf = io.BytesIO()
    compressed.save(buf, format=out_format, quality=85, optimize=True)
    size = buf.tell()
    buf.seek(0)
    return compressed, size

def compress_ibp(gray_pil_img, scale_factor=0.5, iterations=10):
    """
    Aplica compresión y reconstrucción usando Iterative Back Projection (IBP).
    Entrada:
      - gray_pil_img: imagen en escala de grises (PIL)
      - scale_factor: factor de reducción (0 < scale_factor <= 1)
      - iterations: número de iteraciones del algoritmo IBP
    Salida:
      (imagen_reconstruida, tamaño_representación_comprimida_en_bytes)
    """
    if scale_factor <= 0 or scale_factor > 1:
        raise ValueError("scale_factor debe estar en (0,1].")

    img = gray_pil_img.convert("L")
    w, h = img.size
    low_w = max(1, int(round(w * scale_factor)))
    low_h = max(1, int(round(h * scale_factor)))

    # Crear versión low-res (comprimida)
    low_res = img.resize((low_w, low_h), resample=Image.BICUBIC)
    buf = io.BytesIO()
    low_res.save(buf, format="PNG", optimize=True)
    compressed_size = buf.tell()
    buf.seek(0)

    # Inicializar estimado reconstruido (upsampling)
    estimate = low_res.resize((w, h), resample=Image.BICUBIC)
    est_arr = np.asarray(estimate).astype(np.float32)
    low_arr = np.asarray(low_res).astype(np.float32)

    up_factor_w = w / low_w
    up_factor_h = h / low_h
    int_up = (abs(round(up_factor_w) - up_factor_w) < 1e-6) and (abs(round(up_factor_h) - up_factor_h) < 1e-6)
    int_up_w = int(round(up_factor_w))
    int_up_h = int(round(up_factor_h))

    # Proyección inversa iterativa
    for _ in range(iterations):
        simulated_low = np.asarray(
            Image.fromarray(np.clip(est_arr, 0, 255).astype(np.uint8))
            .resize((low_w, low_h), resample=Image.BICUBIC)
        ).astype(np.float32)
        error_low = low_arr - simulated_low

        if int_up:
            error_up = np.repeat(np.repeat(error_low, int_up_h, axis=0), int_up_w, axis=1)
            error_up = error_up[:h, :w]
        else:
            tmp = np.clip(error_low, -255, 255)
            shifted = (tmp + 255).astype(np.uint8)
            up_shifted = np.asarray(
                Image.fromarray(shifted).resize((w, h), resample=Image.BICUBIC)
            ).astype(np.float32)
            error_up = up_shifted - 255.0

        est_arr = np.clip(est_arr + error_up, 0, 255)

    reconstructed = Image.fromarray(est_arr.astype(np.uint8))
    return reconstructed, compressed_size