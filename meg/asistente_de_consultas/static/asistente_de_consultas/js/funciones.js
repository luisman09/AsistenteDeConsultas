// Funciones de validacion de inputs.

// Solo permite ingresar numeros y backspace en el input.
function numeroEnteroPositivo(e){
    var key = window.Event ? e.which : e.keyCode
    return (key >= 48 && key <= 57) || (key == 8)
}

// Solo permite ingresar numeros, punto (.) y backspace en el input.
function numeroRealPositivo(e){
    var key = window.Event ? e.which : e.keyCode
    return (key >= 48 && key <= 57) || (key == 46) || (key == 8)
}

// Solo permite ingresar letras (incluida la ñ), espacio y backspace en el input.
function soloLetras(e){
    var key = window.Event ? e.which : e.keyCode
    return (key >= 65 && key <= 90) || (key >= 97 && key <= 122) || (key == 241) || (key == 209) || (key == 32)  || (key == 8)
}

// Transforma a mayusculas las letas minusculas.
function aMayusculas(obj,id){
    obj = obj.toUpperCase();
    document.getElementById(id).value = obj;
}