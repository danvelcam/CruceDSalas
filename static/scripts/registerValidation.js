function showError(message) {
    var errorContainer = document.getElementById('error-container');
    errorContainer.textContent = message;
    errorContainer.style.display = 'block';
}

function clearErrors() {
    var errorContainer = document.getElementById('error-container');
    errorContainer.textContent = '';
    errorContainer.style.display = 'none';
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
    var dniPattern = /^\d{8}[A-Z]$/;
    if (!dniPattern.test(dni)) {
        showError('El DNI debe tener 8 dígitos y una letra mayúscula');
        return false;
    } 
    return true;
}

function validateTelephoneNumber() {
    var tlf = document.getElementById('id_tlf').value;
    var tlfPattern = /^\d{9}$/;
    if (!tlfPattern.test(tlf)) {
        showError('El teléfono debe tener 9 dígitos');
        return false;
    } 
    return true;
}

function validateForm() {
    clearErrors();
    return validateDNI() && validateTelephoneNumber() && validatePIN();
}