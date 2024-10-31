
from random import randint
import random
import string
from datetime import datetime, timedelta
import uuid

import gspread
from google.oauth2.service_account import Credentials

from insertar_data import InsertData


class RegistroBaseDatos():
        
        def __init__(self, nombre):
              self.n = nombre
      
        def generar_numero_telefono(self):
            prefijo = 52
            
            numero = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            
            return f"{prefijo}{numero}"



        def fecha_actual(self):

            fecha = datetime.now()
            fecha_str = fecha.strftime("%Y-%m-%d")
                
            hora_str = str(fecha.strftime("%H:%M").replace(':', '.'))
            hora_float = float(hora_str)


            return fecha_str, hora_float
        

        def generar_correo_aleatorio(self):
            caracteres_usuario = string.ascii_lowercase + string.digits
            longitud_usuario = random.randint(5, 10)
            usuario = ''.join(random.choice(caracteres_usuario) for _ in range(longitud_usuario))
            
            dominios = ['gmail', 'hotmail', 'yahoo', 'outlook', 'example']
            
            extensiones = ['com', 'net', 'org', 'edu', 'mx']
            
            dominio = random.choice(dominios)
            extension = random.choice(extensiones)
            
            return f"{usuario}@{dominio}.{extension}"

        
        def numeros_aleatorios(self):
               numero = random.randint(1,1000)
               return numero
        


        def convertir_telefono_id(self, numero_telefono):
              numero_str = str(numero_telefono)
              id_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, numero_str))
              return id_uuid


        def tabla_registro_ventas(self):

            numero_secreto = self.numeros_aleatorios()
            nombre = self.n
            telefono = self.generar_numero_telefono()
            direccion = 'En desarollo'
            fecha_registro, hora_registro = self.fecha_actual()


            id_registro_venta = str(numero_secreto) + "-" + telefono[-4:] + '-' + str(hora_registro).replace('.', '')
            id_cliente = self.convertir_telefono_id(telefono)


            hora_confirmacion = 0
            status_registro = 1
            status_confirmacion = 0


            data = [id_registro_venta, id_cliente, numero_secreto, 
                    nombre, telefono, direccion, fecha_registro, 
                    hora_registro, hora_confirmacion, status_registro, status_confirmacion]
            
            insert = InsertData("registro_ventas")
            insert.insert_data(data)

            print('Se registró con exito tu pedido')
        
if __name__=="__main__":
       clase = RegistroBaseDatos("Lucia Roberto Amairani Zomalia Perez")
       clase.tabla_registro_ventas()
