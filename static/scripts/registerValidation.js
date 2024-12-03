var errorContainer = document.getElementById("error-container");

function showError(message) {
    errorContainer.textContent = message
    errorContainer.style.display = 'block';
}

function clearErrors() {
    errorContainer.textContent = '';
    errorContainer.style.display = 'hidden';
}

function validatePIN() {
    var pin = document.getElementById('id_pin').value;
    var repeatPin = document.getElementById('repeat-pin').value;
    if (pin === '' || pin.length !== 4 || isNaN(pin)) {
        showError('El PIN debe tener 4 dígitos');
        return false;
    }
    if (repeatPin === '' || repeatPin.length !== 4 || isNaN(repeatPin)) {
        showError('El PIN debe tener 4 dígitos');
        return false;
    }
    if (pin !== repeatPin) {
        showError('Los PIN no coinciden');
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

function validateTelephoneNumber() {
    var tlf = document.getElementById('id_tlf').value;
    console.log(tlf)
    var tlfPattern = /^\d{9}$/;
    if (!tlfPattern.test(tlf)) {
        showError('El teléfono debe tener 9 dígitos');
        return false;
    } 
    return true;
}
function validateTerms() { 
    var terms = document.getElementById('id_terms').checked;
    if (!terms) {
        showError('Debes aceptar los términos y condiciones');
    }
}

function validateEmail() {
    var email = document.getElementById('id_email').value;
    var emailPattern = /^[\w\.-]+@[\w\.-]+\.\w+$/;
    if (!emailPattern.test(email)) {
        showError('No se ha introducido un email válido');
        return false;
    }
    return true;
}

function validateForm() {
    clearErrors();
    return  validateDNI() && 
    validateEmail() && 
    validateTelephoneNumber() && validatePIN() && 
    validateTerms() ;
}

function loginPIN() {
    var pin = document.getElementById('id_pin').value;
    if (pin.length !== 4) {
        showError('El PIN debe tener 4 dígitos');
        return false;
    }
    return true;
}

function validateLogin() {
    clearErrors();
    return validateEmail() && loginPIN();
} 