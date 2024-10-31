import mysql.connector

from random import randint
import random
import string
from datetime import datetime, timedelta
import uuid


class RegistroVenta():
        
        def __init__(self, nombre):
              self.n = nombre
      
        def generar_numero_telefono(self):
            prefijo = "52"
            
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


        
        def credenciales_sql(self):
                        db = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="Marmansanico12345$$",
                                database="tory_cafe",
                                port="3306")
                        return db



        def tabla_registro_ventas(self):

            db = self.credenciales_sql()

            cursor = db.cursor()

            numero_secreto = 512
            nombre = self.n
            telefono = "526968144662"
            direccion = 'En desarollo'
            fecha_registro, hora_registro = self.fecha_actual()


            id_registro_venta = str(numero_secreto) + "-" + telefono[-4:] + '-' + str(hora_registro).replace('.', '')
            id_cliente = self.convertir_telefono_id(telefono)


            hora_confirmacion = None
            status_registro = True
            status_confirmacion = None


            insert_query = "INSERT INTO registro_ventas (id_registro_ventas, id_cliente, numero_secreto, nombre, telefono, direccion, fecha_registro, hora_registro, hora_confirmacion, status_registro, status_confirmacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (id_registro_venta, id_cliente, numero_secreto, nombre, telefono, direccion, fecha_registro, hora_registro, hora_confirmacion, status_registro, status_confirmacion)
            
            cursor.execute(insert_query, data)

            db.commit()
            db.close()

            print('Se registró con exito tu pedido')

        def consulta_confirmacion(self, telefono, numero_secreto):
            
            db = self.credenciales_sql()
            cursor = db.cursor()

            # Define la consulta para obtener el primer registro agrupado
            # select_query = f"""
            #     SELECT telefono, numero_secreto, nombre, direccion, fecha_registro, hora_registro
            #     FROM (
            #         SELECT *, ROW_NUMBER() OVER (PARTITION BY telefono, numero_secreto, fecha_registro ORDER BY hora_registro DESC) as row_num
            #         FROM registro_ventas
            #     ) as grouped_data
            #     WHERE   row_num = 1
            # """

            query = f"""
                SELECT telefono, numero_secreto, nombre, direccion, fecha_registro, MAX(hora_registro) as ultima_hora_registro
                FROM registro_ventas
                WHERE telefono = '{telefono}' and numero_secreto = {numero_secreto}
                GROUP BY telefono, numero_secreto, nombre, direccion, fecha_registro
                ORDER BY ultima_hora_registro DESC
            """


            # Ejecuta la consulta
            cursor.execute(query)

            # Obtiene los resultados
            resultados = cursor.fetchall()
            print(type(resultados))

            # Cierra la conexión
            db.close()

            # Muestra los resultados
            for registro in resultados:
                print(registro)
        
if __name__=="__main__":
       clase = RegistroVenta('Angel Uriel Chavez Clavellina')
       clase.tabla_registro_ventas()
       clase.consulta_confirmacion('526968144662' , 512)


