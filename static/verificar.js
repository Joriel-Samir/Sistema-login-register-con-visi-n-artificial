// Obtiene referencias a los elementos del DOM
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const capturar = document.getElementById('capturar');
const mensaje = document.getElementById('mensaje');

// Solicita acceso a la cámara y muestra el video en el elemento <video>
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => mensaje.textContent = 'Error al acceder a la cámara: ' + err);

// Cuando el usuario hace clic en "capturar"
capturar.addEventListener('click', () => {
    // Dibuja el frame actual del video en el canvas
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    // Convierte el contenido del canvas a una imagen en base64
    const dataUrl = canvas.toDataURL('image/png');
    // Envía la imagen al backend para verificación facial
    fetch('/verificar-imagen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataUrl })
    })
    .then(res => res.json())
    .then(data => {
        // Muestra el mensaje de respuesta del backend
        mensaje.textContent = data.message;
        // Si la verificación fue exitosa, redirige al inicio después de 2 segundos
        if (data.success) {
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        }
    })
    .catch(err => mensaje.textContent = 'Error al enviar la imagen: ' + err);
});