function inicializar_mensaje_login(mensaje){
    const Toast = Swal.mixin({
        toast: true,
        position: 'bottom-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
      })
      
      Toast.fire({
        icon: 'success',
        title: 'Éxito',
        html: mensaje,
        background: '#ddd'
      })
}