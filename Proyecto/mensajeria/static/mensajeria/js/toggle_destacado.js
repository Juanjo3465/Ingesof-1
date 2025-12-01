function toggleDestacado(mensajeId, btn) {
    fetch(`/mensajeria/toggle-destacado/${mensajeId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.destacado !== undefined) {
            if (data.destacado) {
                btn.classList.add('activo');
            } else {
                btn.classList.remove('activo');
            }
        }
    })
    .catch(error => console.error('Error:', error));
}