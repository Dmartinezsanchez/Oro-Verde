document.addEventListener('DOMContentLoaded', () => {
    var socket = io();  // Conecta con el servidor de Socket.IO

    var messageInput = document.getElementById('messageInput');
    var sendButton = document.getElementById('sendButton');
    var messages = document.getElementById('messages');

    sendButton.addEventListener('click', () => {
        var message = messageInput.value;
        if (message) {
            socket.send(message);  // Envía el mensaje al servidor
            messageInput.value = '';  // Limpia el campo de entrada
        }
    });

    // Escucha los mensajes del servidor y los muestra
    socket.on('message', (msg) => {
        var messageElement = document.createElement('div');
        messageElement.textContent = msg;
        messages.appendChild(messageElement);
    });
});
