"""
Este archivo define la aplicación Flask y sus rutas.

Importa las siguientes funcionalidades de Flask:
- Flask: La clase principal para crear la aplicación.
- render_template: Función para renderizar plantillas HTML.
- request: Objeto para acceder a los datos de la solicitud HTTP.
- redirect: Función para redirigir a una URL diferente.
- url_for: Función para generar URLs para rutas definidas.
- flash: Función para mostrar mensajes a los usuarios.
- jsonify: Función para convertir datos a formato JSON.
- session: Objeto para almacenar datos de sesión del usuario.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,session
from flask_mysqldb import MySQL
import bcrypt
from flask_socketio import SocketIO, send
from config import Config
from functools import wraps
from flask_login import login_required


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages
mysql = MySQL(app)
socketio = SocketIO(app)

# Configuración de la conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'tienda_naturista'

# Ruta del login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes estar registrado e iniciar sesión para acceder a esta sección.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta para cerrar sesion
@app.route('/cerrar_sesion')
def cerrar_sesion():
    """
    Cierra la sesión del usuario y redirige a la página de inicio.
    """
    session.pop('user_id', None)  # Elimina el user_id de la sesión
    flash('Has cerrado sesión exitosamente.', 'success')  # Mensaje de éxito
    return redirect(url_for('index'))  # Redirige al inicio


# Ruta de verificación
@app.route('/ping', methods=['GET'])
def ping():
    """
    Maneja una solicitud para verificar el estado del servidor.

    Esta función responde con un mensaje que indica que el servidor está en funcionamiento.

    Returns:
        Response: Un objeto de respuesta JSON con un mensaje de estado 
        y un código de estado HTTP 200.
    """
    return jsonify({'message': 'Servidor en funcionamiento'}), 200


# Ruta principal
@app.route('/')
def index():
    """
    Renderiza la página de inicio.

    Esta función maneja la solicitud para la página principal de la aplicación y renderiza
    la plantilla `index.html`.

    Returns:
        Response: Un objeto de respuesta que contiene 
        el contenido renderizado de la plantilla `index.html`.
    """
    return render_template('index.html')

@app.route('/admon_productos', methods=['GET', 'POST'])
def admon_productos():
    """
    Maneja la administración de productos en la interfaz de administración.

    Dependiendo de la acción solicitada (Insertar, Actualizar, Borrar, Buscar),
    esta función realiza operaciones correspondientes en la base de datos:
    - Inserta un nuevo producto.
    - Actualiza un producto existente.
    - Borra un producto.
    - Busca un producto por su ID.

    En caso de una acción de búsqueda, el producto encontrado se muestra en un mensaje flash.

    Returns:
        Response: Redirige a la página de administración de productos 
        después de procesar la solicitud.
    """
    producto = None  # Inicializar la variable producto como None para evitar errores
    if request.method == 'POST':
        accion = request.form.get('accion')
        cur = mysql.connection.cursor()
        
        if accion == 'Insertar':
            nombre_producto = request.form.get('nombre_producto')
            valor = request.form.get('valor')
            cantidad = request.form.get('cantidad')  # Obtener cantidad del formulario
            imagen_url = request.form.get('imagen_url')  # Obtener la URL de la imagen
            descripcion = request.form.get('descripcion')  # Obtener descripción del formulario
            cur.execute(
                'INSERT INTO productos (nombre_producto, valor, cantidad, imagen_url, descripcion) '
                'VALUES (%s, %s, %s, %s, %s)', 
                (nombre_producto, valor, cantidad, imagen_url, descripcion)
)

            mysql.connection.commit()
            flash('Producto insertado correctamente!', 'success')
        
        elif accion == 'Actualizar':
            producto_id = request.form.get('producto_id')
            nuevo_nombre = request.form.get('nuevo_nombre')
            nuevo_valor = request.form.get('nuevo_valor')
            # Obtener nueva cantidad del formulario
            nueva_cantidad = request.form.get('nueva_cantidad')

            nueva_imagen_url = request.form.get('nueva_imagen_url')  # Obtener nueva URL de imagen
            nueva_descripcion = request.form.get('nueva_descripcion')  # Obtener nueva descripción
            cur.execute(
                'UPDATE productos SET nombre_producto = %s, valor = %s, cantidad = %s, '
                'imagen_url = %s, descripcion = %s WHERE id = %s',
                (nuevo_nombre, nuevo_valor, nueva_cantidad, nueva_imagen_url, nueva_descripcion, producto_id)
)

            mysql.connection.commit()
            flash('Producto actualizado correctamente!', 'success')
    
        elif accion == 'Borrar':
            producto_id = request.form.get('producto_id')
            cur.execute('DELETE FROM productos WHERE id = %s', (producto_id,))
            mysql.connection.commit()
            flash('Producto borrado correctamente!', 'success')
        
        elif accion == 'Buscar':
            producto_id = request.form.get('producto_id')
            cur.execute('SELECT * FROM productos WHERE id = %s', (producto_id,))
            producto = cur.fetchone()  # Obtener el primer resultado

            if producto: 
                flash(
                    f'Producto encontrado: ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, '
                    f'Valor: {producto[3]}, Imagen URL: {producto[4]}, Descripción: {producto[5]}', 
                    'success'
)

            else:
                flash('Producto no encontrado.', 'danger')

        cur.close()
        return redirect(url_for('admon_productos'))

    return render_template('admon_productos.html', producto=producto)

@app.route('/producto', methods=['POST'])
def crear_producto():
    """
    Crea un nuevo producto en la base de datos.

    Obtiene los detalles del producto del JSON en la solicitud POST y los inserta
    en la base de datos.

    Returns:
        Response: Un objeto JSON con un mensaje de éxito y un código de estado HTTP 201.
    """
    data = request.json
    nombre_producto = data.get('nombre_producto')
    valor = data.get('valor')
    cantidad = data.get('cantidad')
    imagen_url = data.get('imagen_url')
    descripcion = data.get('descripcion')  # Obtener la descripción del JSON

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO productos (nombre_producto, valor, cantidad, imagen_url, descripcion) VALUES (%s, %s, %s, %s, %s)', 
                (nombre_producto, valor, cantidad, imagen_url, descripcion))
    mysql.connection.commit()
    cur.close()

    return jsonify({'mensaje': 'Producto creado correctamente'}), 201

@app.route('/producto/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    """
    Actualiza los detalles de un producto existente en la base de datos.

    Obtiene los detalles actualizados del producto del JSON en la solicitud PUT y 
    actualiza el producto correspondiente en la base de datos.

    Args:
        producto_id (int): El ID del producto que se va a actualizar.

    Returns:
        Response: Un objeto JSON con un mensaje de éxito y un código de estado HTTP 200.
    """
    data = request.json
    nuevo_nombre = data.get('nuevo_nombre')
    nuevo_valor = data.get('nuevo_valor')
    nueva_cantidad = data.get('nueva_cantidad')
    nueva_imagen_url = data.get('nueva_imagen_url')
    nueva_descripcion = data.get('nueva_descripcion')  # Obtener la nueva descripción del JSON

    cur = mysql.connection.cursor()
    cur.execute('UPDATE productos SET nombre_producto = %s, valor = %s, cantidad = %s, imagen_url = %s, descripcion = %s WHERE id = %s', 
                (nuevo_nombre, nuevo_valor, nueva_cantidad, nueva_imagen_url, nueva_descripcion, producto_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'mensaje': 'Producto actualizado correctamente'}), 200

@app.route('/producto/<int:producto_id>', methods=['DELETE'])
def borrar_producto(producto_id):
    """
    Borra un producto de la base de datos.

    Elimina el producto correspondiente al ID proporcionado en la solicitud DELETE.

    Args:
        producto_id (int): El ID del producto que se va a borrar.

    Returns:
        Response: Un objeto JSON con un mensaje de éxito y un código de estado HTTP 200.
    """
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id = %s', (producto_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'mensaje': 'Producto borrado correctamente'}), 200

@app.route('/producto/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
    """
    Muestra los detalles de un producto.

    Obtiene el producto correspondiente al ID proporcionado y renderiza la plantilla 
    `productos.html` con la información del producto.

    Args:
        producto_id (int): El ID del producto para mostrar los detalles.

    Returns:
        Response: La plantilla `productos.html` con los detalles del producto o un objeto JSON
        con un mensaje de error y un código de estado HTTP 404 si el producto no se encuentra.
    """
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE id = %s', (producto_id,))
    producto = cur.fetchone()
    cur.close()

    if producto:
        producto_data = {
            'id': producto[0],
            'nombre': producto[1],
            'cantidad': producto[2],
            'valor': producto[3],
            'descripcion': producto[5],  # Asegúrate de que la descripción esté en el índice correcto
            'imagen_url': producto[4] if producto[4] else 'Imagenes/default.jpeg',
        }
        return render_template('productos.html', producto=producto_data)
    else:
        return jsonify({'mensaje': 'Producto no encontrado'}), 404

@app.route('/buscar_productos', methods=['GET'])
def buscar_productos():
    """
    Busca productos por palabras clave.

    Realiza una búsqueda en la base de datos para encontrar productos que coincidan
    con la consulta proporcionada. Redirige a la página de detalles del producto si se encuentra
    algún resultado, o muestra un mensaje en la plantilla `productos.html` si no se encuentran productos.

    Returns:
        Response: Redirige a la página de detalles del producto si se encuentra un resultado,
        o a la página principal con un mensaje si no se encuentran productos.
    """
    query = request.args.get('query')
    if query:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE nombre_producto LIKE %s', ('%' + query + '%',))
        producto = cur.fetchone()
        cur.close()

        if producto:
            return redirect(url_for('producto_detalle', producto_id=producto[0]))
        else:
            return render_template('productos.html', mensaje="Producto no encontrado")
    return redirect(url_for('index'))


# Ruta para mostrar todos los productos
@app.route('/productos')
def mostrar_productos():
    """
    Muestra una lista de todos los productos en la base de datos.

    Esta función realiza una consulta a la base de datos para obtener todos los productos
    almacenados en la tabla `productos`. Luego, renderiza la plantilla `productos.html`
    y pasa la lista de productos a la plantilla para que sean mostrados.

    Returns:
        Response: La plantilla `productos.html` con la lista de productos.
    """
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    productos = cur.fetchall()
    cur.close()
    return render_template('productos.html', productos=productos)

# Otras rutas


@app.route('/gestion_de_pagos')
@login_required
def gestion_de_pagos():
    """
    Muestra la página de gestión de pagos con el código QR de Nequi.
    Solo accesible para usuarios autenticados.
    """
    # Aquí puedes pasar la URL o la ruta del QR si lo tienes almacenado
    qr_url = url_for('static', filename='Imagenes/Qr.jpeg')  # Asegúrate de colocar tu QR en static/images/
    return render_template('gestion_de_pagos.html', qr_url=qr_url)


@app.route('/nosotros')
def nosotros():
    """
    Renderiza la página de información sobre nosotros.

    Esta función renderiza la plantilla `nosotros.html`, que proporciona información sobre
    la empresa u organización.

    Returns:
        Response: La plantilla `nosotros.html`.
    """
    return render_template('nosotros.html')

@app.route('/promociones')
def promociones():
    """
    Renderiza la página de promociones.

    Esta función renderiza la plantilla `promociones.html`, que muestra las promociones actuales
    o futuras disponibles.

    Returns:
        Response: La plantilla `promociones.html`.
    """
    return render_template('promociones.html')

@app.route('/termin_cond')
def termin_cond():
    """
    Renderiza la página de términos y condiciones.

    Esta función renderiza la plantilla `termin_cond.html`, que presenta los términos y condiciones
    del uso del sitio o servicio.

    Returns:
        Response: La plantilla `termin_cond.html`.
    """
    return render_template('termin_cond.html')

@app.route('/tratam_dat')
def tratam_dat():
    """
    Renderiza la página de tratamiento de datos.

    Esta función renderiza la plantilla `tratam_dat.html`, que detalla la política de tratamiento
    de datos personales.

    Returns:
        Response: La plantilla `tratam_dat.html`.
    """
    return render_template('tratam_dat.html')

@app.route('/user_admon')
def user_admon():
    """
    Renderiza la página de administración de usuarios.

    Esta función renderiza la plantilla `user_admon.html`, que proporciona la interfaz para
    la administración de usuarios del sistema.

    Returns:
        Response: La plantilla `user_admon.html`.
    """
    return render_template('user_admon.html')

# Ruta para registrarse

@app.route('/registrarse', methods=['POST'])
def registrarse():
    """
    Registra un nuevo usuario en el sistema.

    Esta función maneja la solicitud POST para registrar un nuevo usuario. Obtiene los datos
    del formulario (nombre, email y contraseña), asigna el rol por defecto como 'cliente',
    encripta la contraseña utilizando bcrypt, y almacena la información del usuario en la base de datos.

    Después de completar el registro, muestra un mensaje de éxito y redirige al usuario a la página de inicio.

    Returns:
        Response: Redirige a la página principal (`index`) con un mensaje de éxito en un flash.
    """
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    contrasena = request.form.get('contrasena')

    # Asignar el rol por defecto como cliente
    rol = 'cliente'

    hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (nombre, email, contrasena, rol) VALUES (%s, %s, %s, %s)", 
                (nombre, email, hashed_password, rol))
    mysql.connection.commit()
    cur.close()

    flash('Registro exitoso! Puedes iniciar sesión.', 'success')
    return redirect(url_for('index'))

# Ruta para ingresar
@app.route('/ingreso', methods=['POST'])
def ingreso():
    """
    Maneja el inicio de sesión de un usuario.

    Esta función procesa una solicitud POST para autenticar a un usuario. Dependiendo de si la solicitud
    es en formato JSON o formulario, obtiene las credenciales del usuario (nombre y contraseña). Luego,
    verifica si las credenciales están presentes y si son correctas comparando la contraseña ingresada
    con la almacenada en la base de datos.

    Si las credenciales son correctas, almacena el ID del usuario en la sesión y redirige al usuario
    a la página de administración si el rol es 'admin', o a la página principal en caso contrario.
    Si las credenciales son incorrectas o faltan, devuelve un mensaje de error adecuado.

    Returns:
        Response: 
        - Si la solicitud es en formato JSON, devuelve un JSON con un mensaje de éxito o error y un código de estado HTTP.
        - Si la solicitud es en formato de formulario, redirige al usuario a la página correspondiente con un mensaje flash de error si es necesario.
    """
    if request.is_json:
        data = request.get_json()
        usuario = data.get('usuario')
        contrasena = data.get('contrasena')
    else:
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')

    if not usuario or not contrasena:
        if request.is_json:
            return jsonify({'mensaje': 'Faltan credenciales', 'status': 'error'}), 400
        else:
            flash('Faltan credenciales', 'error')
            return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, contrasena, rol FROM usuarios WHERE nombre = %s", [usuario])
    result = cur.fetchone()
    cur.close()

    if not result or not bcrypt.checkpw(contrasena.encode('utf-8'), result[1].encode('utf-8')):
        if request.is_json:
            return jsonify({'mensaje': 'Credenciales incorrectas', 'status': 'error'}), 401
        else:
            flash('Credenciales incorrectas', 'error')
            return redirect(url_for('index'))

    # Credenciales correctas
    user_id = result[0]  # Obtener el ID del usuario
    rol = result[2]      # Obtener el rol del usuario

    # Guardar el user_id en la sesión
    session['user_id'] = user_id

    if request.is_json:
        return jsonify({'mensaje': 'Ingreso exitoso', 'status': 'success'}), 200
    else:
        if rol == 'admin':
            return redirect(url_for('user_admon'))
        else:
            return redirect(url_for('index'))

def user_is_admin():
    """
    Verifica si el usuario actual tiene el rol de administrador.

    Esta función comprueba si el ID del usuario está almacenado en la sesión. Si el ID del usuario está presente,
    realiza una consulta a la base de datos para obtener el rol del usuario. Si el rol del usuario es 'admin', 
    la función devuelve `True`. Si el usuario no es un administrador o no hay un usuario registrado en la sesión, 
    la función devuelve `False`.

    Returns:
        bool: `True` si el usuario actual es un administrador, `False` en caso contrario o si no hay un usuario en sesión.
    """
    if 'user_id' in session:
        user_id = session['user_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT rol FROM usuarios WHERE id = %s", [user_id])
        user = cur.fetchone()
        cur.close()

        if user and user[0] == 'admin':
            return True
    return False

# Ruta para obtener los detalles de un usuario con GET

@app.route('/usuario/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """
    Obtiene los detalles de un usuario específico por su ID.

    Esta función maneja una solicitud GET para recuperar los detalles de un usuario basado en su ID. Realiza
    una consulta a la base de datos para obtener la información del usuario (ID, nombre y correo electrónico).
    Si el usuario es encontrado, devuelve los datos en formato JSON con un código de estado HTTP 200. Si el 
    usuario no se encuentra, devuelve un mensaje de error con un código de estado HTTP 404. En caso de error 
    en la base de datos o en el servidor, devuelve un mensaje de error con un código de estado HTTP 500.

    Args:
        usuario_id (int): El ID del usuario a recuperar.

    Returns:
        Response: 
        - Si el usuario es encontrado, devuelve un JSON con los detalles del usuario y un código de estado HTTP 200.
        - Si el usuario no es encontrado, devuelve un JSON con un mensaje de error y un código de estado HTTP 404.
        - En caso de error en el servidor, devuelve un JSON con un mensaje de error y un código de estado HTTP 500.
    """
    print(f"Obteniendo usuario con ID: {usuario_id}")  # Para depurar
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cur.fetchone()
        cur.close()
    
        print(f"Usuario encontrado: {usuario}")  # Para depurar

        if usuario:
            usuario_data = {
                'id': usuario[0],
                'nombre': usuario[1],
                'email': usuario[2]
            }
            return jsonify(usuario_data), 200
        else:
            return jsonify({'mensaje': 'Usuario no encontrado', 'status': 'error'}), 404

    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return jsonify({'mensaje': 'Error en el servidor', 'status': 'error'}), 500

# Ruta para actualizar un usuario existente con PUT
@app.route('/usuario/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    """
    Actualiza los detalles de un usuario existente por su ID.

    Esta función maneja una solicitud PUT para actualizar los detalles de un usuario basado en su ID. 
    Verifica que la solicitud sea en formato JSON y que contenga los campos requeridos (`nombre` y `email`). 
    Luego, comprueba si el usuario con el ID proporcionado existe. Si el usuario existe, actualiza sus detalles 
    en la base de datos. Si el usuario no se encuentra, devuelve un mensaje de error con un código de estado HTTP 404. 
    En caso de error en la base de datos o en el servidor, devuelve un mensaje de error con un código de estado HTTP 500.

    Args:
        usuario_id (int): El ID del usuario a actualizar.

    Returns:
        Response: 
        - Si la solicitud es válida y el usuario es encontrado y actualizado, devuelve un JSON con un mensaje de éxito y un código de estado HTTP 200.
        - Si la solicitud no es válida o faltan datos requeridos, devuelve un JSON con un mensaje de error y un código de estado HTTP 400.
        - Si el usuario no es encontrado, devuelve un JSON con un mensaje de error y un código de estado HTTP 404.
        - En caso de error en el servidor, devuelve un JSON con un mensaje de error y un código de estado HTTP 500.
    """
    print(f"PUT request received for usuario_id: {usuario_id}")  # Agrega esto para depuración

    # Verificar que los datos se reciban en formato JSON
    if not request.is_json:
        return jsonify({'mensaje': 'Formato de solicitud no válido', 'status': 'error'}), 400

    data = request.json
    nuevo_nombre = data.get('nombre')
    nuevo_email = data.get('email')

    # Verificar que los datos requeridos están presentes
    if not nuevo_nombre or not nuevo_email:
        return jsonify({'mensaje': 'Nombre y correo electrónico son requeridos', 'status': 'error'}), 400

    try:
        cur = mysql.connection.cursor()

        # Verificar si el usuario existe
        cur.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        usuario_existente = cur.fetchone()

        if not usuario_existente:
            cur.close()
            return jsonify({'mensaje': 'Usuario no encontrado', 'status': 'error'}), 404

        # Actualizar el usuario
        cur.execute("UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s", 
                    (nuevo_nombre, nuevo_email, usuario_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({'mensaje': 'Usuario actualizado correctamente', 'status': 'success'}), 200

    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return jsonify({'mensaje': 'Error en el servidor', 'status': 'error'}), 500

# Ruta para eliminar un usuario existente con DELETE
@app.route('/usuario/<int:usuario_id>', methods=['DELETE'])
def borrar_usuario(usuario_id):
    """
    Elimina un usuario existente por su ID.

    Esta función maneja una solicitud DELETE para eliminar un usuario basado en su ID. 
    Primero, verifica si el usuario con el ID proporcionado existe en la base de datos. 
    Si el usuario existe, procede a eliminarlo. Si el usuario no se encuentra, devuelve un mensaje de error 
    con un código de estado HTTP 404. En caso de éxito, devuelve un mensaje de éxito con un código de estado HTTP 200.

    Args:
        usuario_id (int): El ID del usuario a eliminar.

    Returns:
        Response: 
        - Si el usuario es encontrado y eliminado correctamente, devuelve un JSON con un mensaje de éxito y un código de estado HTTP 200.
        - Si el usuario no es encontrado, devuelve un JSON con un mensaje de error y un código de estado HTTP 404.
    """
    cur = mysql.connection.cursor()

    # Verificar si el usuario existe
    cur.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
    usuario_existente = cur.fetchone()

    if not usuario_existente:
        cur.close()
        return jsonify({'mensaje': 'Usuario no encontrado', 'status': 'error'}), 404

    # Borrar el usuario
    cur.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'mensaje': 'Usuario eliminado correctamente', 'status': 'success'}), 200

# Manejador de mensajes enviados desde el chatbox
@socketio.on('message')
def handle_message(msg):
    """
    Maneja los mensajes recibidos desde el chatbox y envía respuestas automáticas.

    Esta función maneja los mensajes recibidos a través del chatbox utilizando Socket.IO. 
    Imprime el mensaje recibido para depuración, luego envía el mensaje a todos los clientes conectados.
    Basado en el contenido del mensaje, envía una respuesta automática a todos los clientes conectados. 
    Las respuestas se generan según las palabras clave detectadas en el mensaje, como "hola", "productos", 
    "adios" y "horarios". Si no se detecta ninguna de estas palabras clave, envía una respuesta genérica.

    Args:
        msg (str): El mensaje recibido desde el chatbox.

    Returns:
        None: Envía el mensaje y la respuesta a todos los clientes conectados.
    """
    print(f"Mensaje recibido: {msg}")
    
    # Envía el mensaje recibido a todos los clientes conectados
    send(msg, broadcast=True)
    
    # Respuestas automáticas basadas en el contenido del mensaje
    if "hola" in msg.lower():
        respuesta = "¡Hola! ¿Cómo puedo ayudarte hoy?"
    elif "productos" in msg.lower():
        respuesta = "Si deseas tener una asesoría personalizada puedes escribir vía WhatsApp al siguiente número 3013817308 y allí ampliaremos la información que requieras."
    elif "adios" in msg.lower():
        respuesta = "¡Hasta luego! No dudes en volver si tienes más preguntas."
    elif "horarios" in msg.lower():
        respuesta = "Nuestro horario de atención es de lunes a viernes, de 9:00 AM a 6:00 PM."
    else:
        respuesta = "No entendí tu mensaje. ¿Podrías reformularlo?"

    send(respuesta)

if __name__ == '__main__':
    socketio.run(app, debug=True)
