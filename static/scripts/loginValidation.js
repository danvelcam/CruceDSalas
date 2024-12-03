var errorContainer = document.getElementById("error-container");

function showError(message) {
    errorContainer.textContent = message
    errorContainer.style.display = 'block';
}

function clearErrors() {
    errorContainer.textContent = '';
    errorContainer.style.display = 'hidden';
}

function loginPIN() {
    var pin = document.getElementById('id_pin').value;
    if (pin.length !== 4) {
        showError('El PIN debe tener 4 dígitos');
        return false;
    }
    return true;
}

function validateDNI() {
    var dni = document.getElementById('id_dni').value;
    console.log(dni)
    var dniPattern = /^\d{8}[A-Z]$/;
    if (!dniPattern.test(dni)) {
        showError('El DNI debe tener 8 dígitos y una letra mayúscula');
        return false;
    } 
    return true;
}


function validateLogin() {
    clearErrors();
    return validateDNI() && loginPIN();
} 