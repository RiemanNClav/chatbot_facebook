from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


from random import randint
import random
import string
from datetime import datetime, timedelta

## CLIENTES REGISTRO
import mysql.connector

##MODULOS
from horarios.horario import Horarios
from direcciones.api import ApiAddress

## ------------------------------VER HORARIO----------------------------------
class ActionGetHorario(Action):

    def name(self) -> Text:
        return "action_get_horario"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        obj = Horarios()
        _, particulares, horario_particular, horario_habitual = obj.print_horario()

        if particulares == '1':
            response = horario_habitual

        else:
            response = horario_habitual
            response += horario_particular
            response += '\n'

        response += "Realiza tu pedido escribiendo 'hacer pedido', de lo contrario consulta otra opción del panel."

        dispatcher.utter_message(text=response)

        return []    
## -----------------------------------ACOTAR UBICACION------------------------------------------

class ActionGetAcotarUbicacion(Action):

    def name(self) -> Text:
        return "action_acotar_ubicacion"
    

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        obj = Horarios()

        disponiblidad, botton = obj.horario()


        if botton == 1:
            disponiblidad += "Perfecto, gracias por tu confianza\n"
            disponiblidad += "\n"
            disponiblidad += "Antes de comenzar con tu pedido, queremos validar tu dirección, ingresala manualmente:\n"
            disponiblidad += "Ej-> alcaldia, colonia, calle"

        dispatcher.utter_message(text=disponiblidad)

        return [] 


## --------------------------------------------HACER PEDIDO-----------------------------------------------------

class ActionGetPedido(Action):

    def name(self) -> Text:
        return "action_registro_nombre"
    

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        api = ApiAddress()
        direccion = tracker.get_slot("direccion")
        try:
            result, radio, distancia = api.bola_cerrada(direccion)
            if result == 1:
                response = "Increible, Si tenemos cobertura hasta tu dirreción!!"
                response += "\n"
                response += "Te comparto brevemente un [link](http://localhost:5056/), por favor llénalo.\n"
                response += "Una vez completado, escribe el NUMERO DE REGISTRO que se te proporcionó:"
            else:
                response = "Lo siento, pero nuestros repartidores locales no llegan hasta tu ubicación :(\n"
                response += "te invito a que hagas tu pedido por uber eats, te comparto brevemente un link, *enviar link*"
        except:
            response = "Lo siento, pero nuestros repartidores locales no llegan hasta tu ubicación :(\n"
            response += "te invito a que hagas tu pedido por uber eats, te comparto brevemente un link, *enviar link*"

        dispatcher.utter_message(text=response)

        return [] 
    
## -----------------------------------------------------------------------------------------------------------------------------

    
class ActionSaveData(Action):
    def name(self) -> Text:
        return "action_save_data"
    

    def obtener_hora_menos_30_min(self):
        hora_actual = datetime.now()
        nueva_hora = hora_actual + timedelta(minutes=30)

        hora = int(nueva_hora.strftime("%H:%M").split(':')[0])


        if hora in list(range(12, 19)):
            return f'{nueva_hora.strftime("%H:%M")} de la tarde'
        elif hora in list(range(19, 24)):
            return f'{nueva_hora.strftime("%H:%M")} de la noche'
        else:
            return f'{nueva_hora.strftime("%H:%M")} de la mañana'
        
    
    def generar_numero_telefono(self):
        prefijo = "+52"
        
        numero = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        
        return f"{prefijo}{numero}"
    

    def generar_correo_aleatorio(self):
        caracteres_usuario = string.ascii_lowercase + string.digits
        longitud_usuario = random.randint(5, 10)
        usuario = ''.join(random.choice(caracteres_usuario) for _ in range(longitud_usuario))
        
        dominios = ['gmail', 'hotmail', 'yahoo', 'outlook', 'example']
        
        extensiones = ['com', 'net', 'org', 'edu', 'mx']
        
        dominio = random.choice(dominios)
        extension = random.choice(extensiones)
        
        return f"{usuario}@{dominio}.{extension}"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name_ = tracker.get_slot("nombre")
        numero_ = tracker.get_slot("numero")
        telefono_ = self.generar_numero_telefono()
        correo_ = self.generar_correo_aleatorio()


        id = numero_ + '-' + telefono_[-4:]
        nombre = name_
        telefono = telefono_
        correo = correo_

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Marmansanico12345$$",
            database="tory_cafe",
            port="3306")

        cursor = db.cursor()

        insert_query = "INSERT INTO clientes (id_cliente, nombre, telefono, correo) VALUES (%s, %s, %s, %s)"
        data = (id, nombre, telefono, correo)
        cursor.execute(insert_query, data)

        db.commit()
        db.close()

        response = f"{nombre}, tu pedido ha quedado registrado, espera máxima de 30 min\n"
        response += f"si no recibes tu pedido antes de las {self.obtener_hora_menos_30_min()}, (siempre y cuando haya sido aceptado)  tu siguiente compra es gratis\n"
        response += f"(si quieres ver el seguimiento, escribe 'seguimiento pedido')"
        response += f"\n"

        dispatcher.utter_message(text=response)
        return []
    

# ------------------------------------------------------------GUARDAR EL NUMERO DE TELEFONO----------------------------------------------------

class ActionSavePhoneNumber(Action):

    def name(self):
        return "action_save_phone_number"

    def run(self, dispatcher, tracker, domain):
        # Obtén el número de teléfono del remitente desde los metadatos del mensaje
        phone_number = tracker.latest_message.get('from')  # Alternativa: puedes revisar tracker.latest_message['metadata'] para Twilio

        if not phone_number:
            # En caso de que no se pueda obtener, tal vez usar un mensaje de error
            dispatcher.utter_message(text="No pude obtener el número de teléfono.")
            return []
        
        dispatcher.utter_message(text=f"Tu numero de telefono es {phone_number}")
        return [SlotSet("phone_number", phone_number)]

if __name__=="__main__":
    h = ActionGetPedido()
    h.prueba()
