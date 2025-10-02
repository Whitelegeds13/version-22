from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_muy_segura_2024'

# Configuración de la base de datos
DATABASE = 'instance/sistema_ventas.db'

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos con todas las tablas necesarias"""
    conn = get_db_connection()
    
    # Crear tablas
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_categoria TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            id_categoria INTEGER,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria)
        );

        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tiendas (
            id_tienda INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_tienda TEXT NOT NULL,
            ubicacion TEXT,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS lugares_entrega (
            id_lugar INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_lugar TEXT NOT NULL,
            direccion TEXT NOT NULL,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            total REAL NOT NULL,
            id_cliente INTEGER,
            id_producto INTEGER,
            id_tienda INTEGER,
            id_lugar INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
            FOREIGN KEY (id_producto) REFERENCES productos (id_producto),
            FOREIGN KEY (id_tienda) REFERENCES tiendas (id_tienda),
            FOREIGN KEY (id_lugar) REFERENCES lugares_entrega (id_lugar)
        );
    ''')
    
    # Insertar datos de ejemplo
    conn.execute("INSERT OR IGNORE INTO categorias (nombre_categoria) VALUES ('Turrones')")
    conn.execute("INSERT OR IGNORE INTO categorias (nombre_categoria) VALUES ('Dulces')")
    conn.execute("INSERT OR IGNORE INTO categorias (nombre_categoria) VALUES ('Chocolates')")
    
    conn.execute("INSERT OR IGNORE INTO tiendas (nombre_tienda, ubicacion) VALUES ('Tienda Principal', 'Centro de la ciudad')")
    conn.execute("INSERT OR IGNORE INTO tiendas (nombre_tienda, ubicacion) VALUES ('Sucursal Norte', 'Zona Norte')")
    
    conn.execute("INSERT OR IGNORE INTO lugares_entrega (nombre_lugar, direccion) VALUES ('Domicilio', 'Entrega a domicilio')")
    conn.execute("INSERT OR IGNORE INTO lugares_entrega (nombre_lugar, direccion) VALUES ('Punto de Recogida', 'Recoger en tienda')")
    
    conn.commit()
    conn.close()

def login_required(f):
    """Decorador para requerir login en las rutas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rutas de autenticación
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id_usuario']
            session['user_name'] = user['nombre']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        
        # Verificar si el email ya existe
        existing_user = conn.execute('SELECT id_usuario FROM usuarios WHERE email = ?', (email,)).fetchone()
        if existing_user:
            flash('El email ya está registrado', 'error')
            conn.close()
            return render_template('register.html')
        
        # Crear nuevo usuario
        hashed_password = generate_password_hash(password)
        conn.execute('INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)',
                    (nombre, email, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    
    # Estadísticas para el dashboard
    stats = {}
    stats['total_productos'] = conn.execute('SELECT COUNT(*) as count FROM productos').fetchone()['count']
    stats['total_clientes'] = conn.execute('SELECT COUNT(*) as count FROM clientes').fetchone()['count']
    stats['total_ventas'] = conn.execute('SELECT COUNT(*) as count FROM ventas').fetchone()['count']
    stats['ingresos_totales'] = conn.execute('SELECT SUM(total) as total FROM ventas').fetchone()['total'] or 0
    
    # Productos con stock bajo
    productos_stock_bajo = conn.execute('SELECT * FROM productos WHERE stock < 10 ORDER BY stock ASC LIMIT 5').fetchall()
    
    # Ventas recientes
    ventas_recientes = conn.execute('''
        SELECT v.*, c.nombre as cliente_nombre, c.apellido as cliente_apellido, 
               p.nombre as producto_nombre
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        JOIN productos p ON v.id_producto = p.id_producto
        ORDER BY v.fecha DESC LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', stats=stats, 
                         productos_stock_bajo=productos_stock_bajo,
                         ventas_recientes=ventas_recientes)

# Rutas de Clientes
@app.route('/clientes')
@login_required
def clientes():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes ORDER BY nombre, apellido').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/nuevo_cliente', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO clientes (nombre, apellido, telefono, direccion) VALUES (?, ?, ?, ?)',
                    (nombre, apellido, telefono, direccion))
        conn.commit()
        conn.close()
        
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('clientes'))
    
    return render_template('nuevo_cliente.html')

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        
        conn.execute('UPDATE clientes SET nombre = ?, apellido = ?, telefono = ?, direccion = ? WHERE id_cliente = ?',
                    (nombre, apellido, telefono, direccion, id))
        conn.commit()
        conn.close()
        
        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('clientes'))
    
    cliente = conn.execute('SELECT * FROM clientes WHERE id_cliente = ?', (id,)).fetchone()
    conn.close()
    
    if not cliente:
        flash('Cliente no encontrado', 'error')
        return redirect(url_for('clientes'))
    
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/eliminar_cliente/<int:id>')
@login_required
def eliminar_cliente(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clientes WHERE id_cliente = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Cliente eliminado exitosamente', 'success')
    return redirect(url_for('clientes'))

# Rutas de Productos
@app.route('/productos')
@login_required
def productos():
    conn = get_db_connection()
    productos = conn.execute('''
        SELECT p.*, c.nombre_categoria 
        FROM productos p 
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
        ORDER BY p.nombre
    ''').fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/nuevo_producto', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        id_categoria = request.form['id_categoria'] if request.form['id_categoria'] else None
        
        conn.execute('INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria) VALUES (?, ?, ?, ?, ?)',
                    (nombre, descripcion, precio, stock, id_categoria))
        conn.commit()
        conn.close()
        
        flash('Producto creado exitosamente', 'success')
        return redirect(url_for('productos'))
    
    categorias = conn.execute('SELECT * FROM categorias ORDER BY nombre_categoria').fetchall()
    conn.close()
    return render_template('nuevo_producto.html', categorias=categorias)

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        id_categoria = request.form['id_categoria'] if request.form['id_categoria'] else None
        
        conn.execute('UPDATE productos SET nombre = ?, descripcion = ?, precio = ?, stock = ?, id_categoria = ? WHERE id_producto = ?',
                    (nombre, descripcion, precio, stock, id_categoria, id))
        conn.commit()
        conn.close()
        
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('productos'))
    
    producto = conn.execute('SELECT * FROM productos WHERE id_producto = ?', (id,)).fetchone()
    categorias = conn.execute('SELECT * FROM categorias ORDER BY nombre_categoria').fetchall()
    conn.close()
    
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos'))
    
    return render_template('editar_producto.html', producto=producto, categorias=categorias)

@app.route('/eliminar_producto/<int:id>')
@login_required
def eliminar_producto(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id_producto = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('productos'))

# Rutas de Categorías
@app.route('/categorias')
@login_required
def categorias():
    conn = get_db_connection()
    categorias = conn.execute('SELECT * FROM categorias ORDER BY nombre_categoria').fetchall()
    conn.close()
    return render_template('categorias.html', categorias=categorias)

@app.route('/nueva_categoria', methods=['GET', 'POST'])
@login_required
def nueva_categoria():
    if request.method == 'POST':
        nombre_categoria = request.form['nombre_categoria']
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO categorias (nombre_categoria) VALUES (?)', (nombre_categoria,))
            conn.commit()
            flash('Categoría creada exitosamente', 'success')
        except sqlite3.IntegrityError:
            flash('Ya existe una categoría con ese nombre', 'error')
        finally:
            conn.close()
        
        return redirect(url_for('categorias'))
    
    return render_template('nueva_categoria.html')

@app.route('/editar_categoria/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre_categoria = request.form['nombre_categoria']
        
        try:
            conn.execute('UPDATE categorias SET nombre_categoria = ? WHERE id_categoria = ?',
                        (nombre_categoria, id))
            conn.commit()
            flash('Categoría actualizada exitosamente', 'success')
        except sqlite3.IntegrityError:
            flash('Ya existe una categoría con ese nombre', 'error')
        finally:
            conn.close()
        
        return redirect(url_for('categorias'))
    
    categoria = conn.execute('SELECT * FROM categorias WHERE id_categoria = ?', (id,)).fetchone()
    conn.close()
    
    if not categoria:
        flash('Categoría no encontrada', 'error')
        return redirect(url_for('categorias'))
    
    return render_template('editar_categoria.html', categoria=categoria)

@app.route('/eliminar_categoria/<int:id>')
@login_required
def eliminar_categoria(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM categorias WHERE id_categoria = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Categoría eliminada exitosamente', 'success')
    return redirect(url_for('categorias'))

# Rutas de Tiendas
@app.route('/tiendas')
@login_required
def tiendas():
    conn = get_db_connection()
    tiendas = conn.execute('SELECT * FROM tiendas ORDER BY nombre_tienda').fetchall()
    conn.close()
    return render_template('tiendas.html', tiendas=tiendas)

@app.route('/nueva_tienda', methods=['GET', 'POST'])
@login_required
def nueva_tienda():
    if request.method == 'POST':
        nombre_tienda = request.form['nombre_tienda']
        ubicacion = request.form['ubicacion']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO tiendas (nombre_tienda, ubicacion) VALUES (?, ?)',
                    (nombre_tienda, ubicacion))
        conn.commit()
        conn.close()
        
        flash('Tienda creada exitosamente', 'success')
        return redirect(url_for('tiendas'))
    
    return render_template('nueva_tienda.html')

# Rutas de Lugares de Entrega
@app.route('/lugares_entrega')
@login_required
def lugares_entrega():
    conn = get_db_connection()
    lugares = conn.execute('SELECT * FROM lugares_entrega ORDER BY nombre_lugar').fetchall()
    conn.close()
    return render_template('lugares_entrega.html', lugares=lugares)

@app.route('/nuevo_lugar_entrega', methods=['GET', 'POST'])
@login_required
def nuevo_lugar_entrega():
    if request.method == 'POST':
        nombre_lugar = request.form['nombre_lugar']
        direccion = request.form['direccion']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO lugares_entrega (nombre_lugar, direccion) VALUES (?, ?)',
                    (nombre_lugar, direccion))
        conn.commit()
        conn.close()
        
        flash('Lugar de entrega creado exitosamente', 'success')
        return redirect(url_for('lugares_entrega'))
    
    return render_template('nuevo_lugar_entrega.html')

@app.route('/editar_lugar_entrega/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_lugar_entrega(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre_lugar = request.form['nombre_lugar']
        direccion = request.form['direccion']
        
        conn.execute('UPDATE lugares_entrega SET nombre_lugar = ?, direccion = ? WHERE id_lugar = ?',
                    (nombre_lugar, direccion, id))
        conn.commit()
        conn.close()
        
        flash('Lugar de entrega actualizado exitosamente', 'success')
        return redirect(url_for('lugares_entrega'))
    
    lugar = conn.execute('SELECT * FROM lugares_entrega WHERE id_lugar = ?', (id,)).fetchone()
    conn.close()
    
    if not lugar:
        flash('Lugar de entrega no encontrado', 'error')
        return redirect(url_for('lugares_entrega'))
    
    return render_template('editar_lugar_entrega.html', lugar=lugar)

# Rutas de Ventas
@app.route('/ventas')
@login_required
def ventas():
    conn = get_db_connection()
    ventas = conn.execute('''
        SELECT v.*, c.nombre as cliente_nombre, c.apellido as cliente_apellido,
               p.nombre as producto_nombre, t.nombre_tienda, l.nombre_lugar
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        JOIN productos p ON v.id_producto = p.id_producto
        JOIN tiendas t ON v.id_tienda = t.id_tienda
        JOIN lugares_entrega l ON v.id_lugar = l.id_lugar
        ORDER BY v.fecha DESC
    ''').fetchall()
    conn.close()
    return render_template('ventas.html', ventas=ventas)

@app.route('/nueva_venta', methods=['GET', 'POST'])
@login_required
def nueva_venta():
    conn = get_db_connection()
    
    if request.method == 'POST':
        id_cliente = int(request.form['id_cliente'])
        id_producto = int(request.form['id_producto'])
        cantidad = int(request.form['cantidad'])
        id_tienda = int(request.form['id_tienda'])
        id_lugar = int(request.form['id_lugar'])
        
        # Obtener el producto para verificar stock y precio
        producto = conn.execute('SELECT * FROM productos WHERE id_producto = ?', (id_producto,)).fetchone()
        
        if not producto:
            flash('Producto no encontrado', 'error')
            conn.close()
            return redirect(url_for('nueva_venta'))
        
        if producto['stock'] < cantidad:
            flash(f'Stock insuficiente. Stock disponible: {producto["stock"]}', 'error')
            conn.close()
            return redirect(url_for('nueva_venta'))
        
        precio_unitario = producto['precio']
        total = precio_unitario * cantidad
        
        # Registrar la venta
        conn.execute('''
            INSERT INTO ventas (id_cliente, id_producto, cantidad, precio_unitario, total, id_tienda, id_lugar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (id_cliente, id_producto, cantidad, precio_unitario, total, id_tienda, id_lugar))
        
        # Actualizar stock del producto
        nuevo_stock = producto['stock'] - cantidad
        conn.execute('UPDATE productos SET stock = ? WHERE id_producto = ?', (nuevo_stock, id_producto))
        
        conn.commit()
        conn.close()
        
        flash('Venta registrada exitosamente', 'success')
        return redirect(url_for('ventas'))
    
    # Obtener datos para el formulario
    clientes = conn.execute('SELECT * FROM clientes ORDER BY nombre, apellido').fetchall()
    productos = conn.execute('SELECT * FROM productos WHERE stock > 0 ORDER BY nombre').fetchall()
    tiendas = conn.execute('SELECT * FROM tiendas ORDER BY nombre_tienda').fetchall()
    lugares = conn.execute('SELECT * FROM lugares_entrega ORDER BY nombre_lugar').fetchall()
    conn.close()
    
    return render_template('nueva_venta.html', clientes=clientes, productos=productos, 
                         tiendas=tiendas, lugares=lugares)

# API para obtener información del producto (AJAX)
@app.route('/api/producto/<int:id>')
@login_required
def api_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id_producto = ?', (id,)).fetchone()
    conn.close()
    
    if producto:
        return jsonify({
            'precio': producto['precio'],
            'stock': producto['stock']
        })
    return jsonify({'error': 'Producto no encontrado'}), 404

# Rutas de Reportes
@app.route('/ganancias')
@login_required
def ganancias():
    conn = get_db_connection()
    
    # Ganancias por mes
    ganancias_mes = conn.execute('''
        SELECT strftime('%Y-%m', fecha) as mes, SUM(total) as total_mes
        FROM ventas
        GROUP BY strftime('%Y-%m', fecha)
        ORDER BY mes DESC
        LIMIT 12
    ''').fetchall()
    
    # Ganancias totales
    total_ganancias = conn.execute('SELECT SUM(total) as total FROM ventas').fetchone()['total'] or 0
    
    # Productos más vendidos
    productos_vendidos = conn.execute('''
        SELECT p.nombre, SUM(v.cantidad) as total_vendido, SUM(v.total) as ingresos
        FROM ventas v
        JOIN productos p ON v.id_producto = p.id_producto
        GROUP BY p.id_producto, p.nombre
        ORDER BY total_vendido DESC
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return render_template('ganancias.html', ganancias_mes=ganancias_mes,
                         total_ganancias=total_ganancias, productos_vendidos=productos_vendidos)

@app.route('/ganancias_producto')
@login_required
def ganancias_producto():
    conn = get_db_connection()
    
    ganancias_producto = conn.execute('''
        SELECT p.nombre, p.precio, SUM(v.cantidad) as total_vendido, 
               SUM(v.total) as ingresos_totales,
               AVG(v.precio_unitario) as precio_promedio
        FROM ventas v
        JOIN productos p ON v.id_producto = p.id_producto
        GROUP BY p.id_producto, p.nombre, p.precio
        ORDER BY ingresos_totales DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('ganancias_producto.html', ganancias_producto=ganancias_producto)

if __name__ == '__main__':
    # Crear el directorio instance si no existe
    os.makedirs('instance', exist_ok=True)
    
    # Inicializar la base de datos
    init_db()
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)

