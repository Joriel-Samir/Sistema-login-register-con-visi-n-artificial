// Obtiene referencias a los elementos del DOM
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const capturar = document.getElementById('capturar');

// Solicita acceso a la cámara y muestra el video en el elemento <video>
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error('Error al acceder a la cámara:', err));

// Cuando el usuario hace clic en "capturar"
capturar.addEventListener('click', () => {
    // Dibuja el video en el canvas
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    // Obtiene la imagen en base64
    const dataUrl = canvas.toDataURL('image/png');
    // Envía la imagen al servidor por fetch
    fetch('/procesar-imagen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataUrl })
    })
    .then(res => res.json())
    .then(data => {
         // Muestra el mensaje de respuesta y redirige al inicio
        alert(data.message);
        window.location.href = '/'; // Redirige al index.html
    })

    .catch(err => alert('Error al enviar la imagen: ' + err));
    
});