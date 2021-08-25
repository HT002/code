function inicializar_mensaje_success(mensaje){
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
      })
      
      Toast.fire({
        icon: 'success',
        title: 'Éxito',
        html: mensaje,
        background: '#eee'
      })
}