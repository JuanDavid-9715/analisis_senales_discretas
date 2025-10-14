// Previsualización de imagen
document.getElementById('id_img').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // Ocultar imagen procesada si está visible
            document.getElementById('processedImage').classList.remove('show');
            
            // Mostrar previsualización
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('previewContainer').classList.add('show');
            
            // Ocultar placeholder
            document.getElementById('placeholderText').style.display = 'none';
        }
        reader.readAsDataURL(file);
    }
});

// Cambiar imagen
function changeImage() {
    // Ocultar previsualización
    document.getElementById('previewContainer').classList.remove('show');
    document.getElementById('id_img').value = '';
    document.getElementById('imagePreview').src = '';
    
    // Mostrar placeholder
    document.getElementById('placeholderText').style.display = 'block';
    
    // Asegurar que la imagen procesada esté oculta
    document.getElementById('processedImage').classList.remove('show');
}

// Prevenir envío si no hay imagen
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    if (!document.getElementById('id_img').files[0]) {
        e.preventDefault();
        alert('Por favor selecciona una imagen');
    }
});