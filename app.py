from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_caminos_de_fe_2026'

# Almacenamiento temporal en memoria
productos = []
clientes = []
proveedores = []
facturas = []

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# ========== PRODUCTOS ==========
@app.route('/productos')
def listar_productos():
    return render_template('productos.html', productos=productos)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        productos.append({
            'nombre': form.nombre.data,
            'categoria': form.categoria.data,
            'cantidad': form.cantidad.data,
            'precio': form.precio.data
        })
        flash('✅ Producto guardado correctamente', 'success')
        return redirect(url_for('listar_productos'))
    return render_template('formulario_producto.html', form=form)

# ========== CLIENTES ==========
@app.route('/clientes')
def listar_clientes():
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        clientes.append({
            'nombre': form.nombre.data,
            'documento': form.documento.data,
            'correo': form.correo.data,
            'direccion': form.direccion.data,
            'telefono': form.telefono.data
        })
        flash('✅ Cliente guardado correctamente', 'success')
        return redirect(url_for('listar_clientes'))
    return render_template('formulario_cliente.html', form=form)

# ========== PROVEEDORES ==========
@app.route('/proveedores')
def listar_proveedores():
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        proveedores.append({
            'nombre_empresa': form.nombre_empresa.data,
            'ruc': form.ruc.data,
            'telefono': form.telefono.data,
            'pais': form.pais.data
        })
        flash('✅ Proveedor guardado correctamente', 'success')
        return redirect(url_for('listar_proveedores'))
    return render_template('formulario_proveedor.html', form=form)

# ========== FACTURACIÓN ==========
@app.route('/facturacion')
def listar_facturacion():
    return render_template('facturacion.html', facturas=facturas)

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def nueva_facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        facturas.append({
            'numero_factura': form.numero_factura.data,
            'fecha_emision': form.fecha_emision.data,
            'cliente': form.cliente.data,
            'total': form.total.data
        })
        flash('✅ Factura emitida correctamente', 'success')
        return redirect(url_for('listar_facturacion'))
    return render_template('formulario_facturacion.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
    