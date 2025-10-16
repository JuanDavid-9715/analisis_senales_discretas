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

document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            // Prevenir scroll cuando el menú está abierto
            document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
        });
        
        // Cerrar menú al hacer clic en un enlace
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
        
        // Cerrar menú al hacer clic fuera
        document.addEventListener('click', function(event) {
            if (!navToggle.contains(event.target) && !navMenu.contains(event.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
});