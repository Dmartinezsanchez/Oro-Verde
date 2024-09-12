from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import bcrypt
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

# Configuración de la conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'tienda_naturista'

mysql = MySQL(app)
socketio = SocketIO(app)

# Ruta de verificación
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Servidor en funcionamiento'}), 200

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la administración de productos
@app.route('/admon_productos', methods=['GET', 'POST'])
def admon_productos():
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
            cur.execute('INSERT INTO productos (nombre_producto, valor, cantidad, imagen_url, descripcion) VALUES (%s, %s, %s, %s, %s)', 
                        (nombre_producto, valor, cantidad, imagen_url, descripcion))
            mysql.connection.commit()
            flash('Producto insertado correctamente!', 'success')
        
        elif accion == 'Actualizar':
            producto_id = request.form.get('producto_id')
            nuevo_nombre = request.form.get('nuevo_nombre')
            nuevo_valor = request.form.get('nuevo_valor')
            nueva_cantidad = request.form.get('nueva_cantidad')  # Obtener nueva cantidad del formulario
            nueva_imagen_url = request.form.get('nueva_imagen_url')  # Obtener nueva URL de imagen
            nueva_descripcion = request.form.get('nueva_descripcion')  # Obtener nueva descripción
            cur.execute('UPDATE productos SET nombre_producto = %s, valor = %s, cantidad = %s, imagen_url = %s, descripcion = %s WHERE id = %s', 
                        (nuevo_nombre, nuevo_valor, nueva_cantidad, nueva_imagen_url, nueva_descripcion, producto_id))
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
                flash(f'Producto encontrado: ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, Valor: {producto[3]}, Imagen URL: {producto[4]}, Descripción: {producto[5]}', 'success')
            else:
                flash('Producto no encontrado.', 'danger')

        cur.close()
        return redirect(url_for('admon_productos'))

    return render_template('admon_productos.html', producto=producto)


# Ruta para crear un nuevo producto con POST
@app.route('/producto', methods=['POST'])
def crear_producto():
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


# Ruta para actualizar un producto existente con PUT
@app.route('/producto/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
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


# Ruta para borrar un producto con DELETE
@app.route('/producto/<int:producto_id>', methods=['DELETE'])
def borrar_producto(producto_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id = %s', (producto_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'mensaje': 'Producto borrado correctamente'}), 200

# Ruta para ver detalles del producto
@app.route('/producto/<int:producto_id>', methods=['GET'])
def producto_detalle(producto_id):
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
    

# Ruta para buscar productos por palabras clave
@app.route('/buscar_productos', methods=['GET'])
def buscar_productos():
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
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    productos = cur.fetchall()
    cur.close()
    return render_template('productos.html', productos=productos)    


# Otras rutas
@app.route('/gestion_de_pagos')
def gestion_de_pagos():
    return render_template('gestion_de_pagos.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/promociones')
def promociones():
    return render_template('promociones.html')

@app.route('/termin_cond')
def termin_cond():
    return render_template('termin_cond.html')

@app.route('/tratam_dat')
def tratam_dat():
    return render_template('tratam_dat.html')

@app.route('/user_admon')
def user_admon():
    return render_template('user_admon.html')

# Ruta para registrarse
@app.route('/registrarse', methods=['POST'])
def registrarse():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    contrasena = request.form.get('contrasena')

    hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (nombre, email, contrasena) VALUES (%s, %s, %s)", (nombre, email, hashed_password))
    mysql.connection.commit()
    cur.close()

    if request.headers.get('X-Test') == 'true':
        # Para pruebas en Postman
        return jsonify({"message": "Registro exitoso! Puedes iniciar sesión."}), 200

    # Para navegadores
    flash('Registro exitoso! Puedes iniciar sesión.', 'success')
    return redirect(url_for('index'))

# Ruta para ingresar

@app.route('/ingreso', methods=['POST'])
def ingreso():
    # Obtener datos dependiendo del tipo de solicitud
    if request.is_json:
        data = request.get_json()
        usuario = data.get('usuario')
        contrasena = data.get('contrasena')
    else:
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')

    # Verificar que se recibieron las credenciales
    if not usuario or not contrasena:
        if request.is_json:
            return jsonify({'mensaje': 'Faltan credenciales', 'status': 'error'}), 400
        else:
            flash('Faltan credenciales', 'error')
            return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT contrasena FROM usuarios WHERE nombre = %s", [usuario])
    result = cur.fetchone()
    cur.close()

    # Verificar credenciales
    if not result or not bcrypt.checkpw(contrasena.encode('utf-8'), result[0].encode('utf-8')):
        if request.is_json:
            return jsonify({'mensaje': 'Credenciales incorrectas', 'status': 'error'}), 401
        else:
            flash('Credenciales incorrectas', 'error')
            return redirect(url_for('index'))

    # Credenciales correctas
    if request.is_json:
        return jsonify({'mensaje': 'Ingreso exitoso', 'status': 'success'}), 200
    else:
        return redirect(url_for('user_admon'))


# Ruta para obtener los detalles de un usuario con GET

@app.route('/usuario/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
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
        return jsonify({'mensaje': 'Error en el servidor', 'status': 'error'}),    


# Ruta para actualizar un usuario existente con PUT
@app.route('/usuario/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
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






