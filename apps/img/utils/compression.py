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

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io

def compress_ibp(gray_pil_img, scale_factor=0.5, iterations=10):
    """
    Aplica compresión y reconstrucción usando Iterative Back Projection (IBP).
    Incluye histograma LBP en la imagen resultante.
    Entrada:
      - gray_pil_img: imagen en escala de grises (PIL)
      - scale_factor: factor de reducción (0 < scale_factor <= 1)
      - iterations: número de iteraciones del algoritmo IBP
    Salida:
      (imagen_reconstruida_con_histograma, tamaño_representación_comprimida_en_bytes)
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
    
    # Aplicar LBP a la imagen reconstruida y generar histograma
    reconstructed_with_histogram = add_lbp_histogram(reconstructed)
    
    return reconstructed_with_histogram, compressed_size

def compute_lbp(image_array):
    """
    Calcula el LBP (Local Binary Pattern) para una imagen en escala de grises.
    """
    height, width = image_array.shape
    lbp = np.zeros_like(image_array)
    
    for i in range(1, height-1):
        for j in range(1, width-1):
            center = image_array[i, j]
            code = 0
            code |= (image_array[i-1, j-1] >= center) << 7
            code |= (image_array[i-1, j] >= center) << 6
            code |= (image_array[i-1, j+1] >= center) << 5
            code |= (image_array[i, j+1] >= center) << 4
            code |= (image_array[i+1, j+1] >= center) << 3
            code |= (image_array[i+1, j] >= center) << 2
            code |= (image_array[i+1, j-1] >= center) << 1
            code |= (image_array[i, j-1] >= center) << 0
            lbp[i, j] = code
    
    return lbp

def add_lbp_histogram(image):
    """
    Añade el histograma LBP a la imagen comprimida.
    """
    # Convertir a array numpy
    img_array = np.array(image)
    
    # Calcular LBP
    lbp_array = compute_lbp(img_array)
    
    # Calcular histograma LBP
    hist, bins = np.histogram(lbp_array.ravel(), bins=256, range=[0, 256])
    
    # Crear una nueva imagen más grande para incluir el histograma
    original_width, original_height = image.size
    new_height = original_height + 150  # Espacio adicional para el histograma
    
    # Crear imagen combinada
    combined_image = Image.new('L', (original_width, new_height), 255)
    combined_image.paste(image, (0, 0))
    
    # Dibujar el histograma
    draw = ImageDraw.Draw(combined_image)
    
    # Normalizar histograma para que quepa en el espacio disponible
    max_hist = max(hist) if max(hist) > 0 else 1
    hist_height = 100
    scale_factor = hist_height / max_hist
    
    # Dibujar ejes
    y_base = original_height + 20
    draw.line([(50, y_base), (50, y_base + hist_height)], fill=0, width=2)  # Eje Y
    draw.line([(50, y_base + hist_height), (original_width - 50, y_base + hist_height)], fill=0, width=2)  # Eje X
    
    # Dibujar barras del histograma (solo los primeros 256 bins)
    bar_width = max(1, (original_width - 100) // 256)
    for i in range(min(256, len(hist))):
        x = 50 + i * bar_width
        bar_height = int(hist[i] * scale_factor)
        if bar_height > 0:
            draw.rectangle([x, y_base + hist_height - bar_height, 
                          x + bar_width - 1, y_base + hist_height], 
                         fill=100)  # Gris medio para las barras
    
    # Añadir título
    try:
        # Intentar usar una fuente por defecto
        font = ImageFont.load_default()
        draw.text((original_width // 2 - 60, original_height + hist_height + 40), 
                 "Histograma LBP", fill=0, font=font)
    except:
        # Si falla la fuente, dibujar sin fuente específica
        draw.text((original_width // 2 - 60, original_height + hist_height + 40), 
                 "Histograma LBP", fill=0)
    
    return combined_image
