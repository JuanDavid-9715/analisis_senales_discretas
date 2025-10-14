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
    
    // Agregar solo los campos de configuración del filtro
    const filterType = document.querySelector('input[name="filter_type"]:checked');
    if (filterType) {
        const filterInput = document.createElement('input');
        filterInput.type = 'hidden';
        filterInput.name = 'filter_type';
        filterInput.value = filterType.value;
        tempForm.appendChild(filterInput);
    }
    
    const cutoff = document.querySelector('input[name="cutoff"]');
    if (cutoff) {
        const cutoffInput = document.createElement('input');
        cutoffInput.type = 'hidden';
        cutoffInput.name = 'cutoff';
        cutoffInput.value = cutoff.value;
        tempForm.appendChild(cutoffInput);
    }
    
    const cutoff2 = document.querySelector('input[name="cutoff2"]');
    if (cutoff2) {
        const cutoff2Input = document.createElement('input');
        cutoff2Input.type = 'hidden';
        cutoff2Input.name = 'cutoff2';
        cutoff2Input.value = cutoff2.value;
        tempForm.appendChild(cutoff2Input);
    }
    
    // Enviar formulario temporal
    document.body.appendChild(tempForm);
    tempForm.submit();
}

// Función para actualizar el valor visual del slider cutoff
function updateCutoffValue() {
    const cutoffSlider = document.querySelector('input[name="cutoff"]');
    const cutoffValue = document.getElementById('cutoffValue');
    if (cutoffSlider && cutoffValue) {
        cutoffValue.textContent = cutoffSlider.value;
    }
}

// Función para actualizar el valor visual del slider cutoff2
function updateCutoff2Value() {
    const cutoff2Slider = document.querySelector('input[name="cutoff2"]');
    const cutoff2Value = document.getElementById('cutoff2Value');
    if (cutoff2Slider && cutoff2Value) {
        cutoff2Value.textContent = cutoff2Slider.value;
    }
}

// Función para mostrar/ocultar el segundo cutoff según el filtro seleccionado
function toggleCutoff2() {
    const cutoff2Field = document.querySelector('input[name="cutoff2"]');
    if (!cutoff2Field) return;
    
    const cutoff2Parent = cutoff2Field.closest('p') || cutoff2Field.parentElement;
    const bandPassSelected = document.querySelector('input[name="filter_type"][value="band_pass"]').checked;
    
    if (cutoff2Parent) {
        cutoff2Parent.style.display = bandPassSelected ? 'block' : 'none';
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si ya hay una imagen procesada
    const processedImage = document.getElementById('processedImage');
    const hasProcessedImage = processedImage && processedImage.classList.contains('show');
    
    // Inicializar valores de los sliders
    updateCutoffValue();
    updateCutoff2Value();
    
    // Configurar visibilidad inicial del cutoff2
    toggleCutoff2();
    
    // Configurar eventos para los sliders (siempre, para actualizar valores visuales)
    const cutoffSlider = document.querySelector('input[name="cutoff"]');
    const cutoff2Slider = document.querySelector('input[name="cutoff2"]');
    
    if (cutoffSlider) {
        cutoffSlider.addEventListener('input', updateCutoffValue);
    }
    
    if (cutoff2Slider) {
        cutoff2Slider.addEventListener('input', updateCutoff2Value);
    }
    
    // Configurar eventos para los radio buttons (siempre, para mostrar/ocultar cutoff2)
    document.querySelectorAll('input[name="filter_type"]').forEach(radio => {
        radio.addEventListener('change', toggleCutoff2);
    });
    
    // Solo configurar eventos de envío automático si hay imagen procesada
    if (hasProcessedImage) {
        // Escuchar cambios en los filtros para envío automático
        document.querySelectorAll('input[name="filter_type"]').forEach(radio => {
            radio.addEventListener('change', function() {
                submitFormWithoutImage();
            });
        });
        
        // Escuchar cambios en los sliders para envío automático (con debounce)
        let sliderTimeout;
        
        if (cutoffSlider) {
            cutoffSlider.addEventListener('input', function() {
                clearTimeout(sliderTimeout);
                sliderTimeout = setTimeout(() => {
                    submitFormWithoutImage();
                }, 500);
            });
        }
        
        if (cutoff2Slider) {
            cutoff2Slider.addEventListener('input', function() {
                clearTimeout(sliderTimeout);
                sliderTimeout = setTimeout(() => {
                    submitFormWithoutImage();
                }, 500);
            });
        }
    }
});