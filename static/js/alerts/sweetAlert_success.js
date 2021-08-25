function inicializar_mensaje_success(mensaje){
    Swal.fire({
        title: 'Éxito',
        html: mensaje,
        icon: 'success',
        backdrop: true,
        position: 'center',
        background: '#eee',
        allowOutsideClick: true,
        allowEscapeKey: true,
        allowEnterKey: true,
        stopKeydownPropagation: false,
    });
}