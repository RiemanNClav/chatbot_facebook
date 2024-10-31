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
from horarios.horario import GoogleDrive
from direcciones.api import ApiAddress
from registro_venta.confirmaciones import RegistrosVentas


api = GoogleDrive()
get_horario = api.action_get_horario()
acotar_ubicacion = api.action_acotar_ubicacion()

dicc = get_horario | acotar_ubicacion

## ------------------------------VER HORARIO----------------------------------  ya quedo
class ActionGetHorario(Action):

    def name(self) -> Text:
        return "action_get_horario"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        api = GoogleDrive()
        dicc = api.action_get_horario()
        particulares = dicc['particulares']
        horario_particular = dicc["horario_particular"]
        horario_habitual = dicc["horario_habitual"]


        response = "HORARIO HABITUAL\n"
        request_horario_habitual = horario_habitual   ##aqui va el request
        for resp in request_horario_habitual:
            response += f"{resp}\n"

        if particulares == ['2']:
            response += "HORARIO PARTICULAR\n"
            request_horario_particular = horario_particular   ##aqui va el request
            for resp in request_horario_particular:
                response += f"{resp}\n"
            
        response += '\n'

        response += "Realiza tu pedido escribiendo 'hacer pedido', de lo contrario consulta otra opción del panel."

        dispatcher.utter_message(text=response)

        return []    
## -----------------------------------ACOTAR UBICACION------------------------------------------

class ActionGetAcotarUbicacion(Action):

    def name(self) -> Text:
        return "action_acotar_ubicacion"
    

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        api = GoogleDrive()
        dicc = api.action_acotar_ubicacion()
        botton = dicc["botton"]
        botton2 = dicc["botton2"]
        dia = dicc["dia"]

        if botton == 1:
            disponiblidad = 'Si tenemos servicio!!\n'
            disponiblidad += "Perfecto, gracias por tu confianza\n"
            disponiblidad += "\n"
            disponiblidad += "Antes de comenzar con tu pedido, queremos validar tu dirección, ingresala manualmente:\n"
            disponiblidad += "Ej-> alcaldia, colonia, calle"

        else:
            if botton2 == 1:
                disponiblidad = f"Aun no tenemos servicio,  te recordamos que nuestro horario es de {dia}, gracias"
            elif botton2 == 2:
                disponiblidad = f"Lo siento, ya hemos cerrado, te recordamos que nuestro servicio fue de {dia}, gracias"


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
                response = "Increible, Si tenemos cobertura hasta tu direción!!"
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
    
## ----------------------------------------------------CONFIRMAR PEDIDO--------------------------------------------

    
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
        

    def fecha_actual(self):
        fecha = datetime.now()
        fecha_str = fecha.strftime("%Y-%m-%d")
                
        hora_str = str(fecha.strftime("%H:%M").replace(':', '.'))
        hora_float = float(hora_str)

        return hora_float
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api = RegistrosVentas("registro_ventas", "Sheet1")
        numero_secreto = tracker.get_slot("numero")
        nombre, id_registro_venta = api.confirmacion_registro_ventas("registro_ventas", numero_secreto, "521295618668")

        if nombre != None:
            api.update_cell_by_id(id_registro_venta, "hora_confirmacion", self.fecha_actual())
            api.update_cell_by_id(id_registro_venta, "status_confirmacion", 1)

            response = f"{nombre}, tu pedido ha quedado registrado, espera máxima de 30 min\n"
            response += f"si no recibes tu pedido antes de las {self.obtener_hora_menos_30_min()}, (siempre y cuando haya sido aceptado)  tu siguiente compra es gratis\n"
            response += f"(si quieres ver el seguimiento, escribe 'seguimiento pedido')"
            response += f"\n"

        else:
            response = "No se ha podido encontrar tu pedido, porfavor vuelve a crear un link, escribiendo 'hacer pedido"


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
