from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from ..forms import IAForm
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import os
from django.conf import settings

# Cargar el modelo
model_path = os.path.join(settings.BASE_DIR, 'apps', 'img', 'model', 'modelo_predecirDigito.h5')
try:
    modelo = tf.keras.models.load_model(model_path)
    MODELO_CARGADO = True
except Exception as e:
    print(f"Error cargando modelo: {e}")
    MODELO_CARGADO = False

def predecir_digito():
    """
    Función mejorada para predecir el dígito desde original_image.jpg
    """
    try:
        # Ruta directa a la imagen original
        imagen_path = os.path.join(settings.MEDIA_ROOT, 'original_image.jpg')
        
        # Cargar y procesar imagen
        imagen = Image.open(imagen_path).convert('L')
        imagen = imagen.resize((28, 28))
        imagen_array = np.array(imagen) / 255.0
        
        # MEJORA 1: Invertir colores si el fondo es claro (como MNIST)
        if np.mean(imagen_array) > 0.5:  # Si el fondo es mayor al 50% blanco
            imagen_array = 1 - imagen_array
        
        # MEJORA 2: Mejorar contraste
        p2, p98 = np.percentile(imagen_array, (2, 98))
        if p98 - p2 > 0:
            imagen_array = np.clip((imagen_array - p2) / (p98 - p2), 0, 1)
        
        # MEJORA 3: Centrar el dígito (opcional)
        imagen_array = np.expand_dims(imagen_array, axis=0)
        imagen_array = np.expand_dims(imagen_array, axis=-1)
        
        # Predecir
        predicciones = modelo.predict(imagen_array, verbose=0)  # verbose=0 para menos logs
        numero_predicho = np.argmax(predicciones[0])
        probabilidad = np.max(predicciones[0])
        
        # MEJORA 4: Agregar advertencia si la confianza es baja
        resultado = {
            'numero': int(numero_predicho),
            'confianza': float(probabilidad),
            'exito': True
        }
        
        if probabilidad < 0.6:  # Umbral de confianza baja
            resultado['advertencia'] = 'Confianza baja - intenta con una imagen más clara'
        
        return resultado
        
    except Exception as e:
        return {
            'numero': None,
            'confianza': 0.0,
            'exito': False,
            'error': str(e)
        }

def ia_view(request):
    if request.method == 'GET':
        return render(request, 'ia.html', {
            'filter_form': IAForm(),
            'modelo_cargado': MODELO_CARGADO
        })

    if request.method == 'POST':
        form = IAForm(request.POST, request.FILES)
        
        if form.is_valid():
            fs = FileSystemStorage()
            
            # Guardar imagen
            if 'img' in request.FILES:
                if fs.exists("original_image.jpg"):
                    fs.delete("original_image.jpg")
                fs.save("original_image.jpg", request.FILES['img'])
            
            # Predecir con IA
            prediccion_ia = predecir_digito() if MODELO_CARGADO else {
                'numero': None,
                'confianza': 0.0,
                'exito': False,
                'error': 'Modelo no disponible'
            }
            
            if prediccion_ia and prediccion_ia['exito']:
                print(f"Número: {prediccion_ia['numero']}, Confianza: {prediccion_ia['confianza']:.4f}")
                if 'advertencia' in prediccion_ia:
                    print(f"Advertencia: {prediccion_ia['advertencia']}")
            elif prediccion_ia:
                print(f"Error en predicción: {prediccion_ia.get('error', 'Error desconocido')}")
            
            return render(request, 'ia.html', {
                'image_uploaded': True,
                'filter_form': form,
                'prediccion_ia': prediccion_ia,
                'modelo_cargado': MODELO_CARGADO
            })
        
        return render(request, 'ia.html', {
            'image_uploaded': False,
            'filter_form': form,
            'modelo_cargado': MODELO_CARGADO
        })