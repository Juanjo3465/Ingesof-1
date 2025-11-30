function buscarApartamentos() {
    const params = new URLSearchParams();
    
    const campos = ['propietario_email', 'interior', 'torre', 'numero'];
    
    campos.forEach(campo => {
        const valor = document.getElementById(campo).value.trim();
        if (valor) {
            params.append(campo, valor);
        }
    });
    
    const queryString = params.toString();
    window.location.href = queryString ? `?${queryString}` : window.location.pathname;
}

function limpiarFiltros() {
    window.location.href = window.location.pathname;
}

document.querySelectorAll('.search-input').forEach(input => {
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            buscarApartamentos();
        }
    });
});
