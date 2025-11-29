// Validaciones para el formulario de editar cuenta

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.edit-form');
    const nombreInput = document.getElementById('nombre');
    const fechaInput = document.getElementById('fecha_nacimiento');
    const correoInput = document.getElementById('correo');
    const celularInput = document.getElementById('celular');

    if (nombreInput) {
        nombreInput.addEventListener('input', function(e) {
            const valor = e.target.value;
            const contieneNumeros = /\d/.test(valor);
            
            if (contieneNumeros) {
                mostrarError(nombreInput, 'El nombre no puede contener números');
            } else {
                limpiarError(nombreInput);
            }
        });
    }

    if (celularInput) {
        celularInput.addEventListener('input', function(e) {
            let valor = e.target.value.replace(/\D/g, '');

            if (valor.length > 10) {
                valor = valor.substring(0, 10);
            }
            
            e.target.value = valor;

            if (valor.length > 0 && valor.length !== 10) {
                mostrarError(celularInput, 'El celular debe tener exactamente 10 dígitos');
            } else {
                limpiarError(celularInput);
            }
        });
    }

    if (correoInput) {
        correoInput.addEventListener('blur', function(e) {
            const valor = e.target.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (valor && !emailRegex.test(valor)) {
                mostrarError(correoInput, 'Ingrese un correo electrónico válido');
            } else {
                limpiarError(correoInput);
            }
        });
    }

    if (fechaInput) {
        fechaInput.addEventListener('change', function(e) {
            const fechaNacimiento = new Date(e.target.value);
            const hoy = new Date();

            let edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
            const mes = hoy.getMonth() - fechaNacimiento.getMonth();
            
            if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNacimiento.getDate())) {
                edad--;
            }

            if (edad < 14) {
                mostrarError(fechaInput, 'Debe tener al menos 14 años');
            } else if (edad > 150) {
                mostrarError(fechaInput, 'La edad no puede ser mayor a 150 años');
            } else {
                limpiarError(fechaInput);
            }
        });
    }

    if (form) {
        form.addEventListener('submit', function(e) {
            let esValido = true;
            let primerError = null;

            if (nombreInput) {
                const nombre = nombreInput.value.trim();
                if (!nombre) {
                    mostrarError(nombreInput, 'El nombre es obligatorio');
                    esValido = false;
                    if (!primerError) primerError = nombreInput;
                } else if (/\d/.test(nombre)) {
                    mostrarError(nombreInput, 'El nombre no puede contener números');
                    esValido = false;
                    if (!primerError) primerError = nombreInput;
                }
            }

            if (fechaInput && fechaInput.value) {
                const fechaNacimiento = new Date(fechaInput.value);
                const hoy = new Date();
                let edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
                const mes = hoy.getMonth() - fechaNacimiento.getMonth();
                
                if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNacimiento.getDate())) {
                    edad--;
                }
                
                if (edad < 14 || edad > 150) {
                    mostrarError(fechaInput, 'La edad debe estar entre 14 y 150 años');
                    esValido = false;
                    if (!primerError) primerError = fechaInput;
                }
            }

            if (correoInput) {
                const correo = correoInput.value.trim();
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!correo) {
                    mostrarError(correoInput, 'El correo es obligatorio');
                    esValido = false;
                    if (!primerError) primerError = correoInput;
                } else if (!emailRegex.test(correo)) {
                    mostrarError(correoInput, 'Ingrese un correo electrónico válido');
                    esValido = false;
                    if (!primerError) primerError = correoInput;
                }
            }

            if (celularInput && celularInput.value) {
                const celular = celularInput.value.trim();
                if (celular && celular.length !== 10) {
                    mostrarError(celularInput, 'El celular debe tener exactamente 10 dígitos');
                    esValido = false;
                    if (!primerError) primerError = celularInput;
                }
            }

            if (!esValido) {
                e.preventDefault();
                if (primerError) {
                    primerError.focus();
                    primerError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    }

    function mostrarError(input, mensaje) {
        limpiarError(input);
        
        input.classList.add('input-error');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'validation-error';
        errorDiv.textContent = mensaje;
        
        input.parentElement.appendChild(errorDiv);
    }

    function limpiarError(input) {
        input.classList.remove('input-error');
        
        const errorExistente = input.parentElement.querySelector('.validation-error');
        if (errorExistente) {
            errorExistente.remove();
        }
    }
});