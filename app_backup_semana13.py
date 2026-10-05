# ==========================================================
# PROYECTO INTEGRADOR - CAMINO DE FE
# Semana 13: Migración a MySQL con CRUD completo
# ==========================================================

import os

from flask import Flask, render_template, redirect, url_for, flash, request

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm


# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

app = Flask(__name__)

app.secret_key = "camino_de_fe_2026"


# ==========================================================
# RUTAS PRINCIPALES
# ==========================================================

@app.route("/")
def inicio():
    return render_template("index.html")


# ==========================================================
# PRODUCTOS
# ==========================================================

@app.route("/productos")
def productos():
    return render_template("productos.html")


@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        flash("Producto registrado correctamente.", "success")

        return redirect(url_for("productos"))

    return render_template(
        "productos_nuevo.html",
        form=form
    )


# ==========================================================
# CLIENTES
# ==========================================================

@app.route("/clientes")
def clientes():
    return render_template("clientes.html")


@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        flash("Cliente registrado correctamente.", "success")

        return redirect(url_for("clientes"))

    return render_template(
        "clientes_nuevo.html",
        form=form
    )


# ==========================================================
# PROVEEDORES
# ==========================================================

@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html")


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        flash("Proveedor registrado correctamente.", "success")

        return redirect(url_for("proveedores"))

    return render_template(
        "proveedores_nuevo.html",
        form=form
    )


# ==========================================================
# FACTURACIÓN
# ==========================================================

@app.route("/facturacion")
def facturacion():
    return render_template("facturacion.html")


@app.route("/facturacion/nuevo", methods=["GET", "POST"])
def nueva_factura():

    if request.method == "POST":

        flash("Factura registrada correctamente.", "success")

        return redirect(url_for("facturacion"))

    return render_template("facturacion_nuevo.html")


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)