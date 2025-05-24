const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const capturar = document.getElementById('capturar');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error('Error al acceder a la cámara:', err));

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
        alert(data.message);
        window.location.href = '/'; // Redirige al index.html
    })
// ...existing
    .catch(err => alert('Error al enviar la imagen: ' + err));
    
});