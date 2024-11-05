from flask import Flask, render_template, request, redirect, session, jsonify, url_for

from insertar_data import  GoogleSheet
from coordenadas import ApiAddress

app = Flask(__name__)

clase =  GoogleSheet('credentials-service-account.json', "registro_ventas", "Sheet1")
api_location = ApiAddress()

app.secret_key = 'mi_clave_secreta_unica_y_segura'

# Ruta para iniciar el registro, que requiere un token
@app.route("/<token>", methods=["GET", "POST"])
def registrar_pedido(token):
    # Guarda el token en la sesión la primera vez que se accede
    session['token'] = token

    if request.method == "POST":
        # Captura los datos del formulario
        nombre = request.form.get("nombre")
        alcaldia = request.form.get("alcaldia")
        colonia = request.form.get("colonia")
        calle = request.form.get("calle")
        cantidad_bebidas = int(request.form.get("cantidad_bebidas"))

        # Guarda la información en la sesión
        session['nombre'] = nombre
        session['alcaldia'] = alcaldia
        session['colonia'] = colonia
        session['calle'] = calle

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

        # Redirige al resumen, pasando el token en la URL
        return redirect(url_for("resumen_pedido", token=token))

    # Renderiza la página inicial si es GET
    return render_template("home.html", token=token)


# Ruta para mostrar el resumen, que también requiere el mismo token
@app.route("/resumen/<token>", methods=["GET", "POST"])
def resumen_pedido(token):
    # # Verifica si el token en la URL coincide con el de la sesión
    # if session.get('token') != token:
    #     return redirect(url_for('error'))  # Redirige a una página de error si el token es inválido

    if request.method == "POST":
        if 'confirmar_pedido' in request.form:
            # Aquí puedes manejar la confirmación, por ejemplo, guardar en una base de datos
            response = f"Pedido confirmado ¡Gracias!\n"
            response += f"NUMERO DE REGISTRO: {session['token']}"
            return response
        elif 'reiniciar' in request.form:
            session.clear()  # Limpiar la sesión para reiniciar el formulario
            return redirect(url_for("registrar_pedido", token=token))

    # Cargar los datos del resumen desde la sesión
    nombre = session.get('nombre')
    # alcaldia = session.get('alcaldia')
    # colonia = session.get('colonia')
    # calle = session.get('calle')

    clase.update_cell_by_id(token, "nombre", nombre)

    latitud = session.get('latitud')
    longitud = session.get('longitud')

    direccion = api_location.api_request_object_1(latitud, longitud)
    _, radio, distancia= api_location.bola_cerrada(latitud, longitud)


    clase.update_cell_by_id(token, "direccion", direccion)
    clase.update_cell_by_id(token, "cobertura", "DENTRO DEL RADIO DE COBERTURA")

    clase.update_cell_by_id(token, "radio_km", radio)
    clase.update_cell_by_id(token, "distancia", distancia)

    bebidas = session.get('bebidas', [])
    
    return render_template("resumen.html", nombre=nombre, direccion=direccion, bebidas=bebidas, token=token)

@app.route('/guardar_ubicacion', methods=['POST'])
def guardar_ubicacion():
    data = request.json
    latitud = data.get("latitud")
    longitud = data.get("longitud")

    print(f"Latitud: {latitud}, Longitud: {longitud}")
    result, radio, distancia= api_location.bola_cerrada(latitud, longitud)
    print(result)
    print(radio)
    print(distancia)

    if result == 1:
        session['latitud'] = latitud
        session['longitud'] = longitud
        return jsonify({"message": "Ubicación recibida correctamente"})
    else:
        return jsonify({"message": "Localmente NO tenemos cobertura hasta tu direccion, favor de pedir por Uber Eats, gracias!"})




# Nueva ruta para guardar el token y generar el enlace único
@app.route('/guardar_token', methods=['POST'])
def guardar_token():
    data = request.json
    token_sesion = data.get('token_sesion')
    # token_sesion = "62a483fc-9d2b-4f44-adf8-9bcea9bd0a14"
    # Genera el enlace único con el token
    enlace = f"https://1a1f-2806-2a0-1220-8638-ccef-71a4-8653-bcb0.ngrok-free.app/{token_sesion}"

    # Aquí puedes guardar el id_registro_venta y el token_sesion en tu base de datos si es necesario.
    # Ejemplo:
    # clase.guardar_token_en_bd(id_registro_venta, token_sesion)

    # Retornar el enlace al chatbot
    return jsonify({"enlace": enlace})


# Página de error si el token no es válido
@app.route('/error')
def error():
    return "Token inválido o ya ha sido usado."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5056)
