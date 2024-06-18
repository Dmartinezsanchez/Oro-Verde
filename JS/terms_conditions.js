document.addEventListener('DOMContentLoaded', function() {
    const termsSection = document.getElementById('terms_section');
    const showMoreBtn = document.getElementById('showMoreBtn');
    const showLessBtn = document.getElementById('showLessBtn');

    showMoreBtn.addEventListener('click', function() {
        termsSection.style.display = 'block';
        showMoreBtn.style.display = 'none';
        showLessBtn.style.display = 'inline-block';
    });

    showLessBtn.addEventListener('click', function() {
        termsSection.style.display = 'none';
        showMoreBtn.style.display = 'inline-block';
        showLessBtn.style.display = 'none';
    });
});

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
