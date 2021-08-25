function inicializar_mensaje_error(mensaje){
    Swal.fire({
        title: 'Algo ha salido mal',
        html: mensaje,
        icon: 'error',
        backdrop: true,
        position: 'center',
        allowOutsideClick: true,
        allowEscapeKey: true,
        allowEnterKey: true,
        stopKeydownPropagation: false,
    });
}