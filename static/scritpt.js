// Obtiene referencias a los elementos del DOM para el contenedor y los botones
const container = document.querySelector('.container')
const registerBtn = document.querySelector('.register-btn')
const loginBtn = document.querySelector('.login-btn')

// Cuando el usuario hace clic en "Registrarse", muestra el formulario de registro
registerBtn.addEventListener('click', () => {
    container.classList.add('active');
});

// Cuando el usuario hace clic en "Iniciar sesión", muestra el formulario de login
loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
});

i