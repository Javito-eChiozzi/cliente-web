
from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os

app = Flask(__name__)
data_file = "clientes.xlsx"

def cargar_datos():
    if os.path.exists(data_file):
        return pd.read_excel(data_file).to_dict(orient="records")
    return []

def guardar_datos(lista):
    df = pd.DataFrame(lista)
    df.to_excel(data_file, index=False)

@app.route("/", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        nuevo = {
            "Cliente": request.form.get("cliente", ""),
            "Estado": request.form.get("estado", ""),
            "Rubro": request.form.get("rubro", ""),
            "Teléfono": request.form.get("telefono", ""),
            "Mail": request.form.get("mail", ""),
            "Comentario": request.form.get("comentario", ""),
            "Zona": request.form.get("zona", ""),
            "Domicilio": request.form.get("domicilio", ""),
            "Localidad": request.form.get("localidad", ""),
            "Provincia": request.form.get("provincia", ""),
            "Comercial": request.form.get("comercial", ""),
            "Contacto": request.form.get("contacto", ""),
            "Departamento Oficina": request.form.get("departamento", ""),
            "Último contacto": request.form.get("ultimo_contacto", ""),
        }
        datos = cargar_datos()
        datos.append(nuevo)
        guardar_datos(datos)
        return redirect("/")

    datos = cargar_datos()
    return render_template("formulario.html", datos=datos)

@app.route("/importar", methods=["GET", "POST"])
def importar():
    if request.method == "POST":
        archivo = request.files.get("archivo")
        if archivo and archivo.filename.endswith(".xlsx"):
            df = pd.read_excel(archivo)
            datos = cargar_datos()
            nuevos = df.to_dict(orient="records")
            datos.extend(nuevos)
            guardar_datos(datos)
            return redirect("/")
    return render_template("importar_excel.html")

@app.route("/descargar")
def descargar():
    return send_file(data_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
