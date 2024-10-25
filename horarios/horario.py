import numpy as np
import os 
import pandas as pd
import re 
from datetime import datetime, timedelta

from dataclasses import dataclass




@dataclass
class HorariosConfig:
        horarios_path: str=os.path.join("horarios.csv")
        horarios_particulares_path: str=os.path.join("horario_particular.txt")


class Horarios:
        def __init__(self):
                self.horarios_config = HorariosConfig()

        def leer_txt_en_lista(self, archivo):

                with open(archivo, 'r') as file:
                        lineas = [linea.strip() for linea in file.readlines()]

                return lineas
        
        def fecha_actual(self):
                
                hora_actual = datetime.now()
                dia_despues = hora_actual - timedelta(days=1)
                hora_actual2 = hora_actual.strftime("%H:%M")
                fecha_actual = hora_actual.strftime("%Y-%m-%d")

                dicc = {
                        'Monday': 'lunes',
                        'Tuesday': 'martes',
                        'Wednesday': 'miércoles',
                        'Thursday': 'jueves',
                        'Friday': 'viernes',
                        'Saturday': 'sábado',
                        'Sunday': 'domingo'}
                
                dia_despues = int(dia_despues.strftime("%Y-%m-%d").split('-')[2])
                fecha_actual = hora_actual.strftime("%Y-%m-%d")
                dia_actual = int(fecha_actual.split('-')[2])
                mes_actual = int(fecha_actual.split('-')[1])
                
                nombre_dia_actual = hora_actual.strftime("%A")
                nombre_dia = dicc[nombre_dia_actual]

                return fecha_actual, dia_actual, nombre_dia, mes_actual, hora_actual2, dia_despues
        
        def fecha_mes_siguiente(self, dia, mes):
                hoy = datetime.now()
                año_actual = hoy.year

                if mes == 12:
                        mes_siguiente = 1
                        año_siguiente = año_actual + 1
                else:
                        mes_siguiente = mes + 1
                        año_siguiente = año_actual
                
                try:
                        fecha_siguiente = datetime(año_siguiente, mes_siguiente, dia)
                        return fecha_siguiente.strftime("%Y-%m-%d")
                except ValueError:
                        return "Fecha no válida (ej. no existe el 30 de febrero)"
        
        def resumir_horarios(self,horarios):
                dias_ordenados = list(horarios.items())
                resumen = []
                inicio = dias_ordenados[0][0]
                anterior_horario = dias_ordenados[0][1]
                for i in range(1, len(dias_ordenados)):
                        dia, horario = dias_ordenados[i]
                        if horario != anterior_horario:
                                if inicio == dias_ordenados[i-1][0]:
                                        resumen.append(f"{inicio} de {anterior_horario}")
                                else:
                                        resumen.append(f"{inicio} a {dias_ordenados[i-1][0]} de {anterior_horario}")
                                
                                inicio = dia
                                
                        anterior_horario = horario
        
                if inicio == dias_ordenados[-1][0]:
                        resumen.append(f"{inicio} de {anterior_horario}")
                else:
                        resumen.append(f"{inicio} a {dias_ordenados[-1][0]} de {anterior_horario}")

                print('HORARIO HABITUAL')
                
                for r in resumen:
                        print(r)

        def expand_days(self, responses: list):
                days_schedule = {}
                print('HORARIO PARTICULAR')
                for response in responses:
                        r = response.replace('[', "").replace("]", "")
                        print(r)
                        pattern = r'\[(.*?)\]'
                        matches = re.findall(pattern, response)
                        
                        date_pattern = r'\w+\s(\d+)'
                        
                        horario = re.search(r'(\d{1,2}am|pm-\d{1,2}pm|am)', response).group(0)
                        
                        for match in matches:
                                dates = re.findall(date_pattern, match)
                                if "al" in match:
                                        start_date = int(dates[0])
                                        end_date = int(dates[1])
                                        
                                        for day in range(start_date, end_date + 1):
                                                days_schedule[day] = horario
                                
                                else:
                                        for date in dates:
                                                day = int(date)
                                                days_schedule[day] = horario
                
        
                return days_schedule
        
        def print_horario(self):
                horarios = pd.read_csv(self.horarios_config.horarios_path)
                horario_general = dict(zip(horarios.dia, horarios.horario_habitual))

                particulares = self.horarios_config.horarios_particulares_path

                self.resumir_horarios(horario_general)
                lista_renglones = self.leer_txt_en_lista(particulares)
                if lista_renglones != []:
                        particulares = self.expand_days(lista_renglones)
                        return horario_general, particulares
                else:
                        return horario_general, '1'
                
        def horario(self):
                fecha_actual_str, dia_actual, nombre_dia, mes_actual, hora_actual, dia_anterior = self.fecha_actual()
                horario_general, particulares = self.print_horario()
                ## QUIERE DECIR QUE NO HAY PARTICULARES
                if particulares == '1':
                        dia = horario_general[nombre_dia]

                else:
                        if dia_actual in list(particulares.keys()):
                                dia = particulares[dia_actual]

                        else:
                                dia = horario_general[nombre_dia]

                                particular_maximo = max(particulares.keys())
                                dia_totales = [i for i in range(0,dia_actual)]
                                fecha_particularidad_siguiente_str = self.fecha_mes_siguiente(dia_actual, mes_actual)
                                fecha_particularidad_siguiente = datetime.strptime(fecha_particularidad_siguiente_str, "%Y-%m-%d")
                                fecha_actual = datetime.strptime(fecha_actual_str, "%Y-%m-%d")
                                diff_fechas = fecha_particularidad_siguiente - fecha_actual
                                # CASO 1 SI DIA ACTUAL > QUE LA PARTICULARIDAD MAXIMA
                                if dia_actual > particular_maximo:
                                        os.remove(self.horarios_config.horarios_particulares_path)

                                # CASO 2: 
                                elif dia_actual <= particular_maximo and (diff_fechas in dia_totales):
                                        os.remove(self.horarios_config.horarios_particulares_path)
                
                print('\n')
                print(f"Hora actual de hoy 14: {hora_actual}")
                print(f"Hora de trabajo para hoy 14: {dia}")


        
if __name__=="__main__":
        obj = Horarios()
        obj.horario()




        # # Expandir los días y asociarles horarios
        # expanded_response1 = expand_days(response1)
        # expanded_response2 = expand_days(response2)
        # expanded_response3 = expand_days(response3)
        # expanded_response4 = expand_days(response4)

        # # Mostrar resultados
        # print("Response 1:", expanded_response1)
        # print("Response 2:", expanded_response2)
        # print("Response 3:", expanded_response3)
        # print("Response 4:", expanded_response4)