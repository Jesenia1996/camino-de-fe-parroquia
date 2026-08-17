from flask import Flask, render_template
import os

app = Flask(__name__)

print("CARPETA DEL PROYECTO:", os.getcwd())
print("EXISTE STATIC:", os.path.exists("static"))
print("EXISTE IMG:", os.path.exists("static/img"))
print("EXISTE PORTADA:", os.path.exists("static/img/portada.jpg"))

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html')

if __name__ == '__main__':
    app.run(debug=True)