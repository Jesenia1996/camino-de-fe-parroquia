import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

import os
import sqlite3

# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_segura_para_desarrollo'

# Ruta de la base de datos SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'ferreteria.db')

def get_db_connection():
    """Establece y retorna una conexión con la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea la carpeta data y la tabla productos si no existen."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
   
    conn.commit()
   
    conn.close()

# Inicializar la base de datos al arrancar la aplicación
init_db()

# Listas en memoria para clientes, proveedores y facturas
lista_clientes = []
lista_proveedores = []
lista_facturas = []


# ==========================================================
# RUTAS DE LA APLICACIÓN
# ==========================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    form = ProductoForm()

    if form.validate_on_submit():
        conn = get_db_connection()
        conn.execute(
            '''INSERT INTO productos (nombre, descripcion, precio, stock, categoria) 
               VALUES (?, ?, ?, ?, ?)''',
            (form.nombre.data, form.descripcion.data, form.precio.data, 
             form.stock.data, form.categoria.data)
        )
        conn.commit()
        conn.close()
        flash('✅ Producto agregado exitosamente.', 'success')
        return redirect(url_for('productos'))

    conn = get_db_connection()
    productos_db = conn.execute('SELECT * FROM productos ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('productos.html', form=form, productos=productos_db)

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', clientes=lista_clientes)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    
    form = ClienteForm()

    if form.validate_on_submit():
     
        lista_clientes.append({
            'nombre': form.nombre.data,
            'documento': form.documento.data,
            'correo': form.correo.data,
            'direccion': form.direccion.data,
            'telefono': form.telefono.data
        })
        flash('✅ Cliente guardado correctamente', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', proveedores=lista_proveedores)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        lista_proveedores.append({
            'nombre_empresa': form.nombre_empresa.data,
            'ruc': form.ruc.data,
            'telefono': form.telefono.data,
            'pais': form.pais.data
        })

        flash('✅ Proveedor guardado correctamente', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', form=form)

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=lista_facturas)

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def nueva_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        lista_facturas.append({
            'numero_factura': form.numero_factura.data,
            'fecha_emision': form.fecha_emision.data,
            'cliente': form.cliente.data,
            'total': form.total.data
        })

        flash('✅ Factura emitida correctamente', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
