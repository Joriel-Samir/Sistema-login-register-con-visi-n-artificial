const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const capturar = document.getElementById('capturar');
const mensaje = document.getElementById('mensaje');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => mensaje.textContent = 'Error al acceder a la cámara: ' + err);

capturar.addEventListener('click', () => {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/png');
    fetch('/verificar-imagen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataUrl })
    })
    .then(res => res.json())
    .then(data => {
        mensaje.textContent = data.message;
        if (data.success) {
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        }
    })
    .catch(err => mensaje.textContent = 'Error al enviar la imagen: ' + err);
});