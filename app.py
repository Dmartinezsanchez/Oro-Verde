from flask import Flask, render_template, request, redirect, url_for, flash
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
            print(f"Datos recibidos - Nombre: {nombre_producto}, Valor: {valor}, Cantidad: {cantidad}, Imagen URL: {imagen_url}")  # Depuración
            cur.execute('INSERT INTO productos (nombre_producto, valor, cantidad, imagen_url) VALUES (%s, %s, %s, %s)', 
                        (nombre_producto, valor, cantidad, imagen_url))
            mysql.connection.commit()
            flash('Producto insertado correctamente!', 'success')
        
        elif accion == 'Actualizar':
            producto_id = request.form.get('producto_id')
            nuevo_nombre = request.form.get('nuevo_nombre')
            nuevo_valor = request.form.get('nuevo_valor')
            nueva_cantidad = request.form.get('nueva_cantidad')  # Obtener nueva cantidad del formulario
            nueva_imagen_url = request.form.get('nueva_imagen_url')  # Obtener nueva URL de imagen
            cur.execute('UPDATE productos SET nombre_producto = %s, valor = %s, cantidad = %s, imagen_url = %s WHERE id = %s', 
                        (nuevo_nombre, nuevo_valor, nueva_cantidad, nueva_imagen_url, producto_id))
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
                flash(f'Producto encontrado: ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, Valor: {producto[3]}, Imagen URL: {producto[4]}', 'success')
            else:
                flash('Producto no encontrado.', 'danger')

        cur.close()
        return redirect(url_for('admon_productos'))

    return render_template('admon_productos.html', producto=producto)

# Nueva ruta para actualizar producto con PUT
@app.route('/producto/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    data = request.json
    nuevo_nombre = data.get('nuevo_nombre')
    nuevo_valor = data.get('nuevo_valor')
    nueva_cantidad = data.get('nueva_cantidad')
    nueva_imagen_url = data.get('nueva_imagen_url')

    cur = mysql.connection.cursor()
    cur.execute('UPDATE productos SET nombre_producto = %s, valor = %s, cantidad = %s, imagen_url = %s WHERE id = %s', 
                (nuevo_nombre, nuevo_valor, nueva_cantidad, nueva_imagen_url, producto_id))
    mysql.connection.commit()
    cur.close()

    return {'mensaje': 'Producto actualizado correctamente'}, 200


# Nueva ruta para borrar producto con DELETE
@app.route('/producto/<int:producto_id>', methods=['DELETE'])
def borrar_producto(producto_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id = %s', (producto_id,))
    mysql.connection.commit()
    cur.close()

    return {'mensaje': 'Producto borrado correctamente'}, 200

# Ruta para ver detalles del producto
@app.route('/producto/<int:producto_id>')
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
            'imagen_url': producto[4] if producto[4] else 'Imagenes/default.jpeg',# Manejo de valores nulos
        }
        return render_template('productos.html', producto=producto_data)
    else:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('index'))

# Otras rutas
@app.route('/gestion_de_pagos')
def gestion_de_pagos():
    return render_template('gestion_de_pagos.html')

@app.route('/informe_ventas')
def informe_ventas():
    return render_template('informe_ventas.html')

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

    flash('Registro exitoso! Puedes iniciar sesión.', 'success')
    return redirect(url_for('index'))

# Ruta para ingresar
@app.route('/ingreso', methods=['POST'])
def ingreso():
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')

    cur = mysql.connection.cursor()
    cur.execute("SELECT contrasena FROM usuarios WHERE nombre = %s", [usuario])
    result = cur.fetchone()
    cur.close()

    if result and bcrypt.checkpw(contrasena.encode('utf-8'), result[0].encode('utf-8')):
        return redirect(url_for('user_admon'))
    else:
        flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
        return redirect(url_for('index'))

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
        respuesta = "Nuestro horario de atención es de 9 AM a 6 PM de lunes a viernes."
    elif "asesoria" in msg.lower():  
        respuesta = "Si deseas una asesoria puedes dejarme tu número telefónico y nos comunicaremos a la mayor brevedad, o si lo prefieres puedes escribir a nuestra linea de whatsaap 3013817308."      
    else:
        respuesta = "No estoy seguro de cómo responder a eso. ¿Podrías ser más específico?, puedes utilizar las siguientes palabras clave: productos, horarios y asesorias"

    # Envía la respuesta automática
    send(respuesta, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)







