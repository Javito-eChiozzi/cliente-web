
from flask import Flask, render_template, request, redirect
import sqlite3
import os
from werkzeug.utils import secure_filename
import openpyxl

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DB_FILE = 'clientes.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                estado TEXT,
                rubro TEXT,
                telefono TEXT,
                mail TEXT,
                comentario TEXT,
                zona TEXT,
                domicilio TEXT,
                localidad TEXT,
                provincia TEXT,
                comercial TEXT,
                contacto TEXT,
                departamento_oficina TEXT,
                ultimo_contacto TEXT
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = [request.form.get(campo) for campo in [
        'cliente', 'estado', 'rubro', 'telefono', 'mail',
        'comentario', 'zona', 'domicilio', 'localidad', 'provincia',
        'comercial', 'contacto', 'departamento_oficina', 'ultimo_contacto'
    ]]
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (
                cliente, estado, rubro, telefono, mail, comentario,
                zona, domicilio, localidad, provincia, comercial,
                contacto, departamento_oficina, ultimo_contacto
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', datos)
        conn.commit()
    return redirect('/ver')

@app.route('/ver')
def ver():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes')
        clientes = cursor.fetchall()
    return render_template('ver_registros.html', clientes=clientes)

@app.route('/importar', methods=['GET', 'POST'])
def importar():
    if request.method == 'POST':
        archivo = request.files['archivo']
        if archivo and archivo.filename.endswith('.xlsx'):
            filename = secure_filename(archivo.filename)
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            archivo.save(ruta)

            wb = openpyxl.load_workbook(ruta)
            hoja = wb.active
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                for i, fila in enumerate(hoja.iter_rows(min_row=2, values_only=True)):
                    if len(fila) >= 14:
                        cursor.execute('''
                            INSERT INTO clientes (
                                cliente, estado, rubro, telefono, mail, comentario,
                                zona, domicilio, localidad, provincia, comercial,
                                contacto, departamento_oficina, ultimo_contacto
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', fila[:14])
                conn.commit()
        return redirect('/ver')
    return render_template('importar.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
