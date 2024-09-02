// Cuando el usuario haga scroll hacia abajo 20px desde la parte superior de la página, mostrar el botón
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("myBtn").style.display = "block";
} else {
    document.getElementById("myBtn").style.display = "none";
}
}

// Cuando el usuario haga click en el botón, hacer scroll hasta la parte superior de la página
function topFunction() {
  document.body.scrollTop = 0; // Para Safari
  document.documentElement.scrollTop = 0; // Para Chrome, Firefox, IE y Opera
}

//  los mensajes desapareceran automáticamente después de unos segundos

document.addEventListener('DOMContentLoaded', function () {
  // Seleccionar todos los elementos con las clases flash-success y flash-error
var flashMessages = document.querySelectorAll('.flash-success, .flash-error');

  // Recorrer todos los mensajes flash seleccionados
flashMessages.forEach(function (message) {
      // Después de 3 segundos (3000 ms), añadir la clase 'fade-out' para iniciar el efecto de desvanecimiento
    setTimeout(function () {
        message.classList.add('fade-out');
      }, 3000); // Ajusta el tiempo antes de que empiece a desaparecer

      // Después de 4 segundos (4000 ms), eliminar el mensaje completamente del DOM
    setTimeout(function () {
        if (message.parentNode) {
            message.parentNode.removeChild(message);
        }
      }, 4000); // Ajusta el tiempo total del efecto
});
});



