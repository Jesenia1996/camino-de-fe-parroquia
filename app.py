# IMPORTANCIONES

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# FORMS
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

#CONEXION MODELO
from conexion.conexion import obtener_conexion
from models import Usuario

# APLICACIÓN 
app = Flask(__name__)

app.secret_key = "camino_de_fe_2026"


# FLASK-LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# PASO 4: LOAD_USER
@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()

    if conexion is None:
        return None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id, usuario, password FROM usuarios WHERE id = %s",
            (user_id,)
        )

        datos = cursor.fetchone()

        if datos:
            return Usuario(
                datos["id"],
                datos["usuario"],
                datos["password"]
            )

        return None

    except Exception as e:
        print("Error al cargar usuario:", e)
        return None

    finally:
        conexion.close()

# ==========================================================
# REGISTRO DE USUARIOS
# ==========================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    # Si ya inició sesión, no necesita registrarse
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = UsuarioForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:

            flash(
                "No se pudo conectar con MySQL.",
                "danger"
            )

            return render_template(
                "registro.html",
                form=form
            )

        try:

            with conexion.cursor() as cursor:

                # Verificar si el usuario ya existe
                cursor.execute(
                    "SELECT id FROM usuarios WHERE usuario = %s",
                    (form.usuario.data,)
                )

                usuario_existente = cursor.fetchone()

                if usuario_existente:

                    flash(
                        "El usuario ya existe. Elija otro nombre.",
                        "warning"
                    )

                    return render_template(
                        "registro.html",
                        form=form
                    )

                # Crear hash seguro de la contraseña
                password_hash = generate_password_hash(
                    form.password.data
                )

                # Guardar usuario en MySQL
                cursor.execute("""
                    INSERT INTO usuarios
                    (usuario, password)
                    VALUES (%s, %s)
                """, (
                    form.usuario.data,
                    password_hash
                ))

            conexion.commit()

            flash(
                "Usuario registrado correctamente. Ahora puede iniciar sesión.",
                "success"
            )

            return redirect(url_for("login"))

        except Exception as e:

            conexion.rollback()

            print("Error al registrar usuario:", e)

            flash(
                "No se pudo registrar el usuario.",
                "danger"
            )

        finally:

            conexion.close()

    return render_template(
        "registro.html",
        form=form
    )

# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # Si ya inició sesión, ir directamente al dashboard
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:

            flash(
                "No se pudo conectar con MySQL.",
                "danger"
            )

            return render_template(
                "login.html",
                form=form
            )

        try:

            with conexion.cursor() as cursor:

                cursor.execute("""
                    SELECT id, usuario, password
                    FROM usuarios
                    WHERE usuario = %s
                """, (
                    form.usuario.data,
                ))

                datos = cursor.fetchone()

            # Verificar usuario y contraseña
            if datos and check_password_hash(
                datos["password"],
                form.password.data
            ):

                usuario = Usuario(
                    datos["id"],
                    datos["usuario"],
                    datos["password"]
                )

                login_user(usuario)

                flash(
                    "Inicio de sesión correcto.",
                    "success"
                )

                return redirect(url_for("dashboard"))

            else:

                flash(
                    "Usuario o contraseña incorrectos.",
                    "danger"
                )

        except Exception as e:

            print("Error al iniciar sesión:", e)

            flash(
                "Ocurrió un error al iniciar sesión.",
                "danger"
            )

        finally:

            conexion.close()

    return render_template(
        "login.html",
        form=form
    )

# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )

# ==========================================================
# CERRAR SESIÓN
# ==========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))

# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def index():
    return render_template("index.html")


# ==========================================================
# PRODUCTOS
# ==========================================================

@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con MySQL.", "danger")
        return render_template("productos.html", productos=[])

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id, nombre, descripcion, precio, stock
                FROM productos
                ORDER BY id DESC
            """)

            productos = cursor.fetchall()

        return render_template(
            "productos.html",
            productos=productos
        )

    except Exception as e:

        print("Error al consultar productos:", e)

        flash("Ocurrió un error al consultar los productos.", "danger")

        return render_template(
            "productos.html",
            productos=[]
        )

    finally:

        conexion.close()


# ----------------------------------------------------------
# NUEVO PRODUCTO
# ----------------------------------------------------------

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:

            flash("No se pudo conectar con MySQL.", "danger")

            return render_template(
                "formulario_producto.html",
                form=form
            )

        try:

            with conexion.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO productos
                    (nombre, descripcion, precio, stock)
                    VALUES (%s, %s, %s, %s)
                """, (
                    form.nombre.data,
                    form.descripcion.data,
                    form.precio.data,
                    form.stock.data
                ))

            conexion.commit()

            flash(
                "Producto registrado correctamente.",
                "success"
            )

            return redirect(url_for("productos"))

        except Exception as e:

            conexion.rollback()

            print("Error al registrar producto:", e)

            flash(
                "No se pudo registrar el producto.",
                "danger"
            )

        finally:

            conexion.close()

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ----------------------------------------------------------
# EDITAR PRODUCTO
# ----------------------------------------------------------

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return redirect(url_for("productos"))

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id, nombre, descripcion, precio, stock
                FROM productos
                WHERE id = %s
            """, (id,))

            producto = cursor.fetchone()

        if producto is None:

            flash("El producto no existe.", "warning")

            return redirect(url_for("productos"))

        form = ProductoForm()

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    UPDATE productos
                    SET nombre = %s,
                        descripcion = %s,
                        precio = %s,
                        stock = %s
                    WHERE id = %s
                """, (
                    form.nombre.data,
                    form.descripcion.data,
                    form.precio.data,
                    form.stock.data,
                    id
                ))

            conexion.commit()

            flash(
                "Producto actualizado correctamente.",
                "success"
            )

            return redirect(url_for("productos"))

        if not form.is_submitted():

            form.nombre.data = producto["nombre"]
            form.descripcion.data = producto["descripcion"]
            form.precio.data = producto["precio"]
            form.stock.data = producto["stock"]

        return render_template(
            "formulario_producto.html",
            form=form
        )

    except Exception as e:

        conexion.rollback()

        print("Error al editar producto:", e)

        flash(
            "No se pudo actualizar el producto.",
            "danger"
        )

        return redirect(url_for("productos"))

    finally:

        conexion.close()


# ----------------------------------------------------------
# ELIMINAR PRODUCTO
# ----------------------------------------------------------

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return redirect(url_for("productos"))

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                "DELETE FROM productos WHERE id = %s",
                (id,)
            )

        conexion.commit()

        flash(
            "Producto eliminado correctamente.",
            "success"
        )

    except Exception as e:

        conexion.rollback()

        print("Error al eliminar producto:", e)

        flash(
            "No se pudo eliminar el producto.",
            "danger"
        )

    finally:

        conexion.close()

    return redirect(url_for("productos"))


# ==========================================================
# CLIENTES
# ==========================================================

@app.route("/clientes")
@login_required
def clientes():

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return render_template(
            "clientes.html",
            clientes=[]
        )

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id, nombre, cedula, telefono, correo
                FROM clientes
                ORDER BY id DESC
            """)

            clientes = cursor.fetchall()

        return render_template(
            "clientes.html",
            clientes=clientes
        )

    except Exception as e:

        print("Error al consultar clientes:", e)

        flash(
            "Ocurrió un error al consultar los clientes.",
            "danger"
        )

        return render_template(
            "clientes.html",
            clientes=[]
        )

    finally:

        conexion.close()


# ----------------------------------------------------------
# NUEVO CLIENTE
# ----------------------------------------------------------

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:

            flash("No se pudo conectar con MySQL.", "danger")

            return render_template(
                "formulario_cliente.html",
                form=form
            )

        try:

            with conexion.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO clientes
                    (nombre, cedula, telefono, correo)
                    VALUES (%s, %s, %s, %s)
                """, (
                    form.nombre.data,
                    form.cedula.data,
                    form.telefono.data,
                    form.correo.data
                ))

            conexion.commit()

            flash(
                "Cliente registrado correctamente.",
                "success"
            )

            return redirect(url_for("clientes"))

        except Exception as e:

            conexion.rollback()

            print("Error al registrar cliente:", e)

            flash(
                "No se pudo registrar el cliente.",
                "danger"
            )

        finally:

            conexion.close()

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# ----------------------------------------------------------
# EDITAR CLIENTE
# ----------------------------------------------------------

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return redirect(url_for("clientes"))

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id, nombre, cedula, telefono, correo
                FROM clientes
                WHERE id = %s
            """, (id,))

            cliente = cursor.fetchone()

        if cliente is None:

            flash("El cliente no existe.", "warning")

            return redirect(url_for("clientes"))

        form = ClienteForm()

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    UPDATE clientes
                    SET nombre = %s,
                        cedula = %s,
                        telefono = %s,
                        correo = %s
                    WHERE id = %s
                """, (
                    form.nombre.data,
                    form.cedula.data,
                    form.telefono.data,
                    form.correo.data,
                    id
                ))

            conexion.commit()

            flash(
                "Cliente actualizado correctamente.",
                "success"
            )

            return redirect(url_for("clientes"))

        if not form.is_submitted():

            form.nombre.data = cliente["nombre"]
            form.cedula.data = cliente["cedula"]
            form.telefono.data = cliente["telefono"]
            form.correo.data = cliente["correo"]

        return render_template(
            "formulario_cliente.html",
            form=form
        )

    except Exception as e:

        conexion.rollback()

        print("Error al editar cliente:", e)

        flash(
            "No se pudo actualizar el cliente.",
            "danger"
        )

        return redirect(url_for("clientes"))

    finally:

        conexion.close()


# ----------------------------------------------------------
# ELIMINAR CLIENTE
# ----------------------------------------------------------

@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):

    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM clientes WHERE id = %s",
            (id,)
        )

        conexion.commit()

        flash("Cliente eliminado correctamente.", "success")

    except Exception as e:

        conexion.rollback()

        print("Error al eliminar cliente:", e)

        # Error 1451: el cliente tiene facturas asociadas
        if e.args and e.args[0] == 1451:

            flash(
                "No se puede eliminar este cliente porque tiene facturas asociadas.",
                "warning"
            )

        else:

            flash(
                "No se pudo eliminar el cliente.",
                "danger"
            )

    finally:
        conexion.close()

    return redirect(url_for("clientes"))


# ==========================================================
# PROVEEDORES
# ==========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return render_template(
            "proveedores.html",
            proveedores=[]
        )

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id, nombre, telefono, correo
                FROM proveedores
                ORDER BY id DESC
            """)

            proveedores = cursor.fetchall()

        return render_template(
            "proveedores.html",
            proveedores=proveedores
        )

    except Exception as e:

        print("Error al consultar proveedores:", e)

        flash(
            "Ocurrió un error al consultar los proveedores.",
            "danger"
        )

        return render_template(
            "proveedores.html",
            proveedores=[]
        )

    finally:

        conexion.close()


# ----------------------------------------------------------
# NUEVO PROVEEDOR
# ----------------------------------------------------------

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:

            flash("No se pudo conectar con MySQL.", "danger")

            return render_template(
                "formulario_proveedor.html",
                form=form
            )

        try:

            with conexion.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO proveedores
                    (nombre, telefono, correo)
                    VALUES (%s, %s, %s)
                """, (
                    form.nombre.data,
                    form.telefono.data,
                    form.correo.data
                ))

            conexion.commit()

            flash(
                "Proveedor registrado correctamente.",
                "success"
            )

            return redirect(url_for("proveedores"))

        except Exception as e:

            conexion.rollback()

            print("Error al registrar proveedor:", e)

            flash(
                "No se pudo registrar el proveedor.",
                "danger"
            )

        finally:

            conexion.close()

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ----------------------------------------------------------
# EDITAR PROVEEDOR
# ----------------------------------------------------------

@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return redirect(url_for("proveedores"))

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id, nombre, telefono, correo
                FROM proveedores
                WHERE id = %s
            """, (id,))

            proveedor = cursor.fetchone()

        if proveedor is None:

            flash("El proveedor no existe.", "warning")

            return redirect(url_for("proveedores"))

        form = ProveedorForm()

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    UPDATE proveedores
                    SET nombre = %s,
                        telefono = %s,
                        correo = %s
                    WHERE id = %s
                """, (
                    form.nombre.data,
                    form.telefono.data,
                    form.correo.data,
                    id
                ))

            conexion.commit()

            flash(
                "Proveedor actualizado correctamente.",
                "success"
            )

            return redirect(url_for("proveedores"))

        if not form.is_submitted():

            form.nombre.data = proveedor["nombre"]
            form.telefono.data = proveedor["telefono"]
            form.correo.data = proveedor["correo"]

        return render_template(
            "formulario_proveedor.html",
            form=form
        )

    except Exception as e:

        conexion.rollback()

        print("Error al editar proveedor:", e)

        flash(
            "No se pudo actualizar el proveedor.",
            "danger"
        )

        return redirect(url_for("proveedores"))

    finally:

        conexion.close()


# ----------------------------------------------------------
# ELIMINAR PROVEEDOR
# ----------------------------------------------------------

@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return redirect(url_for("proveedores"))

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                "DELETE FROM proveedores WHERE id = %s",
                (id,)
            )

        conexion.commit()

        flash(
            "Proveedor eliminado correctamente.",
            "success"
        )

    except Exception as e:

        conexion.rollback()

        print("Error al eliminar proveedor:", e)

        flash(
            "No se pudo eliminar el proveedor.",
            "danger"
        )

    finally:

        conexion.close()

    return redirect(url_for("proveedores"))


# ==========================================================
# FACTURACIÓN
# ==========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return render_template(
            "facturacion.html",
            facturas=[]
        )

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT
                    f.id,
                    f.fecha,
                    f.cliente_id,
                    c.nombre AS cliente_nombre,
                    f.total
                FROM facturacion f
                LEFT JOIN clientes c
                    ON f.cliente_id = c.id
                ORDER BY f.id DESC
            """)

            facturas = cursor.fetchall()

        return render_template(
            "facturacion.html",
            facturas=facturas
        )

    except Exception as e:

        print("Error al consultar facturas:", e)

        flash(
            "Ocurrió un error al consultar las facturas.",
            "danger"
        )

        return render_template(
            "facturacion.html",
            facturas=[]
        )

    finally:

        conexion.close()


# ----------------------------------------------------------
# NUEVA FACTURA
# ----------------------------------------------------------

@app.route("/facturacion/nuevo", methods=["GET", "POST"])
@login_required
def nueva_factura():

    form = FacturacionForm()

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return render_template(
            "formulario_facturacion.html",
            form=form
        )

    try:

        # --------------------------------------------------
        # CARGAR CLIENTES EN EL SELECT
        # --------------------------------------------------

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id, nombre
                FROM clientes
                ORDER BY nombre
            """)

            clientes = cursor.fetchall()

        form.cliente_id.choices = [
            (cliente["id"], cliente["nombre"])
            for cliente in clientes
        ]

        # --------------------------------------------------
        # GUARDAR FACTURA
        # --------------------------------------------------

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO facturacion
                    (cliente_id, total)
                    VALUES (%s, %s)
                """, (
                    form.cliente_id.data,
                    form.total.data
                ))

            conexion.commit()

            flash(
                "Factura registrada correctamente.",
                "success"
            )

            return redirect(url_for("facturacion"))

        return render_template(
            "formulario_facturacion.html",
            form=form
        )

    except Exception as e:

        conexion.rollback()

        print("Error al registrar factura:", e)

        flash(
            "No se pudo registrar la factura.",
            "danger"
        )

        return render_template(
            "formulario_facturacion.html",
            form=form
        )

    finally:

        conexion.close()

# ----------------------------------------------------------
# EDITAR FACTURA
# ----------------------------------------------------------

@app.route("/facturacion/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_factura(id):

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con PostgreSQL.", "danger")
        return redirect(url_for("facturacion"))

    try:

        # --------------------------------------------------
        # BUSCAR FACTURA
        # --------------------------------------------------

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id, cliente_id, total
                FROM facturacion
                WHERE id = %s
            """, (id,))

            factura = cursor.fetchone()

        if factura is None:

            flash("La factura no existe.", "warning")

            return redirect(url_for("facturacion"))


        # --------------------------------------------------
        # CREAR FORMULARIO
        # --------------------------------------------------

        form = FacturacionForm()


        # --------------------------------------------------
        # CARGAR CLIENTES
        # --------------------------------------------------

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id, nombre
                FROM clientes
                ORDER BY nombre
            """)

            clientes = cursor.fetchall()


        form.cliente_id.choices = [
            (cliente["id"], cliente["nombre"])
            for cliente in clientes
        ]


        # --------------------------------------------------
        # ACTUALIZAR FACTURA
        # --------------------------------------------------

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    UPDATE facturacion
                    SET cliente_id = %s,
                        total = %s
                    WHERE id = %s
                """, (
                    form.cliente_id.data,
                    form.total.data,
                    id
                ))

            conexion.commit()

            flash(
                "Factura actualizada correctamente.",
                "success"
            )

            return redirect(url_for("facturacion"))


        # --------------------------------------------------
        # CARGAR DATOS ACTUALES
        # --------------------------------------------------

        if not form.is_submitted():

            form.cliente_id.data = factura["cliente_id"]
            form.total.data = factura["total"]


        return render_template(
            "formulario_facturacion.html",
            form=form
        )


    except Exception as e:

        conexion.rollback()

        print("Error al editar factura:", e)

        flash(
            "No se pudo actualizar la factura.",
            "danger"
        )

        return redirect(url_for("facturacion"))


    finally:

        conexion.close()
        
# ----------------------------------------------------------
# ELIMINAR FACTURA
# ----------------------------------------------------------

@app.route("/facturacion/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_factura(id):

    conexion = obtener_conexion()

    if conexion is None:

        flash("No se pudo conectar con MySQL.", "danger")

        return redirect(url_for("facturacion"))

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                "DELETE FROM facturacion WHERE id = %s",
                (id,)
            )

        conexion.commit()

        flash(
            "Factura eliminada correctamente.",
            "success"
        )

    except Exception as e:

        conexion.rollback()

        print("Error al eliminar factura:", e)

        flash(
            "No se pudo eliminar la factura.",
            "danger"
        )

    finally:

        conexion.close()

    return redirect(url_for("facturacion"))


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)
