from flask import Flask, render_template, request, redirect, session

from registro_venta_drive import RegistroBaseDatos

app = Flask(__name__)
app.secret_key = 'clave_secreta'

clase = RegistroBaseDatos()
numero_secreto = clase.numeros_aleatorios()


@app.route("/", methods=["GET", "POST"])
def registrar_pedido():
    if request.method == "POST":
        # Captura los datos del formulario
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        cantidad_bebidas = int(request.form.get("cantidad_bebidas"))

        # Guarda la información en la sesión
        session['nombre'] = nombre
        session['direccion'] = direccion
        session['telefono'] = telefono
        bebidas = []

        # Captura las bebidas seleccionadas
        for i in range(cantidad_bebidas):
            bebida = {
                'tipo_bebida': request.form.get(f"tipo_bebida_{i}"),
                'tipo_leche': request.form.get(f"tipo_leche_{i}"),
                'azucar': request.form.get(f"azucar_{i}")
            }
            bebidas.append(bebida)

        session['bebidas'] = bebidas

        # Redirige al resumen
        return redirect("/resumen")

    # Renderiza la página inicial si es GET
    return render_template("home.html")


@app.route("/resumen", methods=["GET", "POST"])
def resumen_pedido():
    clase = RegistroBaseDatos()
    if request.method == "POST":
        if 'confirmar_pedido' in request.form:
            # Aquí puedes manejar la confirmación, por ejemplo, guardar en una base de datos
            response = f"Pedido confirmado ¡Gracias!\n"
            response += f"NUMERO DE REGISTRO: {numero_secreto}"
            return response
        elif 'reiniciar' in request.form:
            session.clear()  # Limpiar la sesión para reiniciar el formulario
            return redirect("/")

    # Cargar los datos del resumen desde la sesión
    nombre = session.get('nombre')
    direccion = session.get('direccion')
    telefono = session.get('telefono')
    bebidas = session.get('bebidas', [])
    
    clase.tabla_registro_ventas(nombre, direccion, telefono, numero_secreto)



    return render_template("resumen.html", nombre=nombre, direccion=direccion, telefono=telefono, bebidas=bebidas)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5056)