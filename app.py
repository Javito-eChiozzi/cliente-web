from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'clientes.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
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
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = (
        request.form['cliente'],
        request.form['estado'],
        request.form['rubro'],
        request.form['telefono'],
        request.form['mail'],
        request.form['comentario'],
        request.form['zona'],
        request.form['domicilio'],
        request.form['localidad'],
        request.form['provincia'],
        request.form['comercial'],
        request.form['contacto'],
        request.form['departamento_oficina'],
        request.form['ultimo_contacto']
    )
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (
            cliente, estado, rubro, telefono, mail, comentario,
            zona, domicilio, localidad, provincia, comercial,
            contacto, departamento_oficina, ultimo_contacto
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', datos)
    conn.commit()
    conn.close()
    return redirect('/ver')

@app.route('/ver')
def ver():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    registros = cursor.fetchall()
    columnas = [description[0] for description in cursor.description]
    conn.close()
    return render_template('ver_registros.html', registros=registros, columnas=columnas)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if request.method == 'POST':
        datos = (
            request.form['cliente'],
            request.form['estado'],
            request.form['rubro'],
            request.form['telefono'],
            request.form['mail'],
            request.form['comentario'],
            request.form['zona'],
            request.form['domicilio'],
            request.form['localidad'],
            request.form['provincia'],
            request.form['comercial'],
            request.form['contacto'],
            request.form['departamento_oficina'],
            request.form['ultimo_contacto'],
            id
        )
        cursor.execute('''
            UPDATE clientes SET
                cliente=?, estado=?, rubro=?, telefono=?, mail=?, comentario=?,
                zona=?, domicilio=?, localidad=?, provincia=?, comercial=?,
                contacto=?, departamento_oficina=?, ultimo_contacto=?
            WHERE id=?
        ''', datos)
        conn.commit()
        conn.close()
        return redirect('/ver')

    cursor.execute("SELECT * FROM clientes WHERE id=?", (id,))
    registro = cursor.fetchone()
    conn.close()
    columnas = ['cliente', 'estado', 'rubro', 'telefono', 'mail', 'comentario',
                'zona', 'domicilio', 'localidad', 'provincia', 'comercial',
                'contacto', 'departamento_oficina', 'ultimo_contacto']
    return render_template('editar.html', registro=registro, columnas=columnas)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/ver')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
