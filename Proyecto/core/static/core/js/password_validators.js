(function() {
    const nuevaPassword = document.getElementById('nuevaPassword');
    const confirmarPassword = document.getElementById('confirmarPassword');
    const form = document.getElementById('passwordForm');

    // Requisitos de validación
    const requirements = {
        length: { regex: /.{8,}/, element: document.getElementById('req-length') },
        uppercase: { regex: /[A-Z]/, element: document.getElementById('req-uppercase') },
        lowercase: { regex: /[a-z]/, element: document.getElementById('req-lowercase') },
        number: { regex: /[0-9]/, element: document.getElementById('req-number') },
        special: { regex: /[@$!%*?&#]/, element: document.getElementById('req-special') },
        space: { regex: /^\S*$/, element: document.getElementById('req-space') }
    };

    const matchRequirement = document.getElementById('req-match');

    // Validar contraseña en tiempo real
    if (nuevaPassword) {
        nuevaPassword.addEventListener('input', function() {
            validatePassword();
            validateMatch();
        });
    }

    // Validar coincidencia de contraseñas
    if (confirmarPassword) {
        confirmarPassword.addEventListener('input', function() {
            validateMatch();
        });
    }

    function validatePassword() {
        const password = nuevaPassword.value;

        // Validar cada requisito
        for (let key in requirements) {
            const req = requirements[key];
            const isValid = req.regex.test(password);
            
            if (password.length === 0) {
                req.element.classList.remove('valid', 'invalid');
                req.element.style.color = 'rgba(51, 51, 51, 0.6)';
                req.element.style.fontWeight = '400';
            } else if (isValid) {
                req.element.classList.add('valid');
                req.element.classList.remove('invalid');
                req.element.style.color = '#3d7a52';
                req.element.style.fontWeight = '500';
            } else {
                req.element.classList.add('invalid');
                req.element.classList.remove('valid');
                req.element.style.color = '#a84e4e';
                req.element.style.fontWeight = '500';
            }
        }
    }

    function validateMatch() {
        const password = nuevaPassword.value;
        const confirmPassword = confirmarPassword.value;

        if (confirmPassword.length === 0) {
            matchRequirement.classList.remove('valid', 'invalid');
            matchRequirement.style.color = 'rgba(51, 51, 51, 0.6)';
            matchRequirement.style.fontWeight = '400';
        } else if (password === confirmPassword && password.length > 0) {
            matchRequirement.classList.add('valid');
            matchRequirement.classList.remove('invalid');
            matchRequirement.style.color = '#3d7a52';
            matchRequirement.style.fontWeight = '500';
        } else {
            matchRequirement.classList.add('invalid');
            matchRequirement.classList.remove('valid');
            matchRequirement.style.color = '#a84e4e';
            matchRequirement.style.fontWeight = '500';
        }
    }

    // Validar antes de enviar
    if (form) {
        form.addEventListener('submit', function(e) {
            const password = nuevaPassword.value;
            const confirmPassword = confirmarPassword.value;
            let errors = [];

            // Validar todos los requisitos
            if (password.length < 8) {
                errors.push('La contraseña debe tener al menos 8 caracteres');
            }
            if (!/[A-Z]/.test(password)) {
                errors.push('La contraseña debe contener al menos una mayúscula');
            }
            if (!/[a-z]/.test(password)) {
                errors.push('La contraseña debe contener al menos una minúscula');
            }
            if (!/[0-9]/.test(password)) {
                errors.push('La contraseña debe contener al menos un número');
            }
            if (!/[@$!%*?&#]/.test(password)) {
                errors.push('La contraseña debe contener al menos un carácter especial (@$!%*?&#)');
            }
            if (/\s/.test(password)) {
                errors.push('La contraseña no puede contener espacios');
            }
            if (password !== confirmPassword) {
                errors.push('Las contraseñas no coinciden');
            }

            // Si hay errores, prevenir envío y mostrar
            if (errors.length > 0) {
                e.preventDefault();
                alert(errors.join('\n'));
            }
        });
    }
})();