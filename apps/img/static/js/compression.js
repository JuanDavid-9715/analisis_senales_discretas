// Función para enviar formulario SIN imagen (solo configuración)
function submitFormWithoutImage() {
    // Crear formulario temporal sin campo de imagen
    const originalForm = document.getElementById('uploadForm');
    const tempForm = document.createElement('form');
    tempForm.method = 'POST';
    tempForm.enctype = 'multipart/form-data';
    tempForm.action = originalForm.action;
    
    // Agregar CSRF token
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
    tempForm.appendChild(csrfInput);
    
    // Agregar solo el campo de porcentaje de compresión
    const compressionSlider = document.querySelector('input[name="compression_percentage"]');
    if (compressionSlider) {
        const compressionInput = document.createElement('input');
        compressionInput.type = 'hidden';
        compressionInput.name = 'compression_percentage';
        compressionInput.value = compressionSlider.value;
        tempForm.appendChild(compressionInput);
    }
    
    // Enviar formulario temporal
    document.body.appendChild(tempForm);
    tempForm.submit();
}

// Función para actualizar el valor visual del slider de compresión
function updateCompressionValue() {
    const compressionSlider = document.querySelector('input[name="compression_percentage"]');
    const compressionValue = document.getElementById('compressionValue');
    if (compressionSlider && compressionValue) {
        compressionValue.textContent = compressionSlider.value;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si ya hay una imagen procesada
    const processedImage = document.getElementById('processedImage');
    const hasProcessedImage = processedImage && processedImage.classList.contains('show');
    
    // Inicializar valor del slider
    updateCompressionValue();
    
    // Configurar evento para el slider (siempre, para actualizar valor visual)
    const compressionSlider = document.querySelector('input[name="compression_percentage"]');
    if (compressionSlider) {
        compressionSlider.addEventListener('input', updateCompressionValue);
    }
    
    // Solo configurar eventos de envío automático si hay imagen procesada
    if (hasProcessedImage) {
        // Escuchar cambios en el slider para envío automático (con debounce)
        let sliderTimeout;
        
        if (compressionSlider) {
            compressionSlider.addEventListener('input', function() {
                clearTimeout(sliderTimeout);
                sliderTimeout = setTimeout(() => {
                    submitFormWithoutImage();
                }, 500);
            });
        }
    }
});