function inicializar_mensaje_success(mensaje){
    Swal.fire({
        title: 'Éxito',
        html: mensaje,
        icon: 'success',
        backdrop: true,
        position: 'center',
        allowOutsideClick: false,
        allowEscapeKey: true,
        allowEnterKey: true,
        stopKeydownPropagation: false,
    });
}