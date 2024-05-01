document.getElementById("mostrar-mas-datos1").addEventListener("click", function() {
    document.getElementById("datos1").style.maxHeight = "none"; // Muestra el párrafo completo
    document.getElementById("mostrar-mas-datos1").style.display = "none"; // Oculta el botón "Mostrar más"
    document.getElementById("mostrar-menos-datos1").style.display = "inline-block"; // Muestra el botón "Mostrar menos"
});

document.getElementById("mostrar-menos-datos1").addEventListener("click", function() {
    document.getElementById("datos1").style.maxHeight = "50px"; // Oculta el párrafo completo
    document.getElementById("mostrar-mas-datos1").style.display = "inline-block"; // Muestra el botón "Mostrar más"
    document.getElementById("mostrar-menos-datos1").style.display = "none"; // Oculta el botón "Mostrar menos"
});

document.getElementById("mostrar-mas-datos2").addEventListener("click", function() {
    document.getElementById("datos2").style.maxHeight = "none"; 
    document.getElementById("mostrar-mas-datos2").style.display = "none"; 
    document.getElementById("mostrar-menos-datos2").style.display = "inline-block"; 
});

document.getElementById("mostrar-menos-datos2").addEventListener("click", function() {
    document.getElementById("datos2").style.maxHeight = "50px"; 
    document.getElementById("mostrar-mas-datos2").style.display = "inline-block"; 
    document.getElementById("mostrar-menos-datos2").style.display = "none";
});

document.getElementById("mostrar-mas-datos3").addEventListener("click", function() {
    document.getElementById("datos3").style.maxHeight = "none"; 
    document.getElementById("mostrar-mas-datos3").style.display = "none";
    document.getElementById("mostrar-menos-datos3").style.display = "inline-block"; 
});

document.getElementById("mostrar-menos-datos3").addEventListener("click", function() {
    document.getElementById("datos3").style.maxHeight = "10px"; 
    document.getElementById("mostrar-mas-datos3").style.display = "inline-block";
    document.getElementById("mostrar-menos-datos3").style.display = "none";
});
document.getElementById("mostrar-mas").addEventListener("click", function() {
    document.getElementById("datos3").style.maxHeight = "none"; 
    document.getElementById("mostrar-mas").style.display = "none";
    document.getElementById("mostrar-menos").style.display = "inline-block"; 
});

document.getElementById("mostrar-menos").addEventListener("click", function() {
    document.getElementById("datos3").style.maxHeight = "10px"; 
    document.getElementById("mostrar-mas").style.display = "inline-block";
    document.getElementById("mostrar-menos").style.display = "none";
});